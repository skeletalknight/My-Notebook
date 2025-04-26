import re
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class ReplacePlugin(BasePlugin):
    """
    MkDocs 插件，默认使用正则表达式替换 Markdown 文档中的文本
    """
    
    config_scheme = (
        ('replacements', config_options.Type(dict, default={})),
        ('use_regex', config_options.Type(bool, default=False)),  # 添加是否使用正则的开关
    )
    
    def on_page_markdown(self, markdown, page, config, files):
        """
        在 Markdown 被处理前执行文本替换
        """
        replacements = self.config.get('replacements', {})
        use_regex = self.config.get('use_regex', True)
        
        for pattern, replacement in replacements.items():
            if use_regex:
                # 正则表达式替换
                markdown = re.sub(pattern, replacement, markdown)
            else:
                # 普通文本替换
                markdown = markdown.replace(pattern, replacement)
        
        return markdown
    
#搜索文件夹下面所有的md文件，将里面其中所有形如