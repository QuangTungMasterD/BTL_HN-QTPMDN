{
    'name': 'AI Assistant',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Chatbot AI có thể truy vấn dữ liệu Odoo',
    'depends': ['base', 'base_automation', 'mail', 'web'],
    'data': [
        # 'views/chat_window.xml',
        # 'views/menu.xml',
    ],
    # 'qweb': ['static/src/xml/chat_template.xml'],
    'assets': {
        'web.assets_backend': [
            'ai_assistant/static/src/js/chat_widget.js',
            'ai_assistant/static/src/css/chat_widget.css',
            'ai_assistant/static/src/xml/chat_widget.xml',
        ],
    },
    'installable': True,
    'application': False,
}