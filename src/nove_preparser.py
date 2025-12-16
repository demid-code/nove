from pathlib import Path

from nove_error import report_error
from nove_lexer import TokenType, Token, Lexer
from nove_ops import WORD_TO_OPTYPE

class PreParser:
    def __init__(self, tokens: list[Token], include_paths: list[Path] = [], included_paths: list[Path] = []):
        self.tokens = tokens
        self.current = 0

        # include paths
        self.include_paths = include_paths

        # paths that already have been included
        self.included_paths = included_paths

        self.macros = {}

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)
    
    def advance(self) -> tuple[Token, int]:
        idx = self.current
        self.current += 1
        return (self.tokens[idx], idx)

    def peek(self, ahead: int = 0) -> Token:
        if self.current + ahead >= len(self.tokens): return None
        return self.tokens[self.current + ahead]

    def make_macro(self, macro_token: Token, macro_idx: int):
        if self.is_at_end():
            report_error("Expected macro name", macro_token.loc)

        name_token, name_idx = self.advance()
        if name_token.type != TokenType.WORD:
            report_error("Expected macro name to be a valid word", name_token.loc)

        if name_token.text in WORD_TO_OPTYPE:
            report_error(f"`{name_token.text}` is illegal macro name", name_token.loc)

        found_macroend = False
        while not self.is_at_end():
            tok, _ = self.advance()
            if tok.type == TokenType.WORD:
                if tok.text == "endmacro":
                    found_macroend = True
                    break

                if tok.text == "macro":
                    break

        if found_macroend:
            macro_tokens = self.tokens[name_idx + 1:self.current - 1]
            self.macros[name_token.text] = {"tokens": macro_tokens}
            self.tokens = self.tokens[:macro_idx] + self.tokens[self.current:]
            self.current -= len(macro_tokens) + 3
        else:
            report_error("Expected `endmacro` to close macro definition", macro_token.loc)

    def insert_macro(self, token: Token, token_idx: int):
        macro_tokens = self.macros[token.text]["tokens"]

        self.tokens[token_idx:token_idx + 1] = macro_tokens
        self.current = token_idx + len(macro_tokens)

    def include_file(self, include_token: Token, include_idx: int):
        if self.is_at_end():
            report_error("Expected a path to include", include_token.loc)
        
        path_token, path_idx = self.advance()
        if path_token.type != TokenType.STRING:
            report_error("Expected path to be a valid string", path_token.loc)

        part_path = Path(path_token.text[1:-1])

        for ipath in self.include_paths:
            final_path = ipath.joinpath(part_path).resolve()
            
            if not final_path.exists(): continue

            if final_path in self.included_paths:
                self.tokens[include_idx:include_idx + 2] = []
                self.current = include_idx
                return

            self.included_paths.append(final_path)

            included_tokens = Lexer(final_path).lex()
            included_tokens, included_macros = PreParser(included_tokens, self.include_paths + [final_path], self.included_paths).pre_parse()

            self.macros.update(included_macros)
            self.tokens[include_idx:include_idx + 2] = included_tokens
            # self.current = include_idx + len(included_tokens)
            self.current = include_idx

            return

    def scan_token(self):
        token, token_idx = self.advance()

        if token.type == TokenType.WORD:
            # macros
            if token.text == "macro": self.make_macro(token, token_idx)
            if token.text in self.macros: self.insert_macro(token, token_idx)

            # including
            if token.text == "include": self.include_file(token, token_idx)

    def pre_parse(self) -> tuple[list[Token], dict[str, dict]]:
        while not self.is_at_end():
            self.scan_token()

        return (self.tokens, self.macros)