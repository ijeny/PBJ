import re

class Template:
    def __init__(self, text):
        self.text = text
        self.pattern = re.compile(r'{%(.*?)%}', re.DOTALL)

    def render(self, context=None):
        if context is None:
            context = {}

        # pastikan _POST selalu ada
        context.setdefault('_POST', {})

        output = []

        def emit(value):
            output.append(str(value))

        context['emit'] = emit

        code = []
        code.append("def __template_func__():")
        code.append("    pass")  # placeholder

        pos = 0
        for match in self.pattern.finditer(self.text):
            html = self.text[pos:match.start()]
            if html:
                code.append(f"    emit({html!r})")

            block = match.group(1)
            for line in block.splitlines():
                if line.strip():
                    code.append("    " + line)
            pos = match.end()

        rest = self.text[pos:]
        if rest:
            code.append(f"    emit({rest!r})")

        script = "\n".join(code)

        exec(script, context)
        context['__template_func__']()

        return "".join(output)
