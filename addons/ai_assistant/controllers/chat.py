import json
import requests
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class AIChatController(http.Controller):

    @http.route('/ai/chat', type='json', auth='user', methods=['POST'], csrf=False)
    def chat(self, **kwargs):
        """Nhận câu hỏi từ client, xử lý và trả về kết quả"""
        question = kwargs.get('message', '')
        if not question:
            return {'error': 'Không có câu hỏi'}

        # Lấy API key Gemini
        api_key = request.env['ir.config_parameter'].sudo().get_param('gemini_api_key')
        if not api_key:
            return {'error': 'Chưa cấu hình Gemini API Key!'}

        # Bước 1: Gọi Gemini để phân tích ý định và trích xuất tham số
        intent_data = self._parse_intent(question, api_key)
        if not intent_data or 'error' in intent_data:
            # Nếu không phân tích được, trả về câu trả lời mặc định
            return self._fallback_response(question, api_key)

        _logger.error(f"Intent = ===============: {intent_data}")
        # Bước 2: Thực thi truy vấn dựa trên intent
        result = self._execute_query(intent_data)
        if not result:
            return {'response': 'Xin lỗi, không tìm thấy dữ liệu phù hợp.'}

        # Bước 3: Dùng Gemini để tạo câu trả lời tự nhiên từ kết quả
        final_response = self._format_response(question, result, api_key)
        return {'response': final_response}

    def _parse_intent(self, question, api_key):
        """Gửi prompt để xác định intent và tham số"""
        prompt = f"""
Bạn là trợ lý AI. CHỈ được chọn model trong danh sách sau:
- 'hr.employee'
- 'du_an'
- 'cong_viec'
- 'khach_hang'

KHÔNG được để model rỗng.

Phân tích câu hỏi và trả JSON:
- intent: 'count' hoặc 'list'
- model: bắt buộc chọn 1 trong danh sách trên
- domain: []
- fields: ['name']

Câu hỏi: "{question}"

Ví dụ:
- "Có bao nhiêu nhân viên?" → {{"intent":"count","model":"hr.employee","domain":[]}}
- "Có bao nhiêu dự án?" → {{"intent":"count","model":"du_an","domain":[]}}
- "Có bao nhiêu công việc?" → {{"intent":"count","model":"cong_viec","domain":[]}}
- "Liệt kê khách hàng?" → {{"intent":"list","model":"khach_hang","domain":[]}}

Chỉ trả JSON.
"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code != 200:
                return {'error': f'Lỗi Gemini: {response.text}'}
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            # Lấy phần JSON từ text (có thể có thêm markdown)
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if not json_match:
                return {'error': 'Không phân tích được intent'}
            intent_data = json.loads(json_match.group())
            
            return intent_data
        except Exception as e:
            _logger.exception("Lỗi parse intent")
            return {'error': str(e)}

    def _execute_query(self, intent_data):
        """Thực thi truy vấn dựa trên intent"""
        _logger.error("=== _execute_query called")
        model_name = intent_data.get('model')
        if not model_name:
            return None
        try:
            model = request.env[model_name]
        except KeyError:
            _logger.error(f"Model không tồn tại: {model_name}")
            return None

        domain = intent_data.get('domain', [])
        intent = intent_data.get('intent')
        _logger.error(f"intent: {intent}")
        _logger.error(f"intent: {domain}")
        result = None
        if intent == 'count':
            count = model.search_count(domain)
            result = {'count': count}
        elif intent == 'list':
            fields = intent_data.get('fields', ['name'])
            records = model.search(domain)
            data = []
            for rec in records:
                row = {}
                for f in fields:
                    # Lấy giá trị của trường, nếu là Many2one thì lấy tên
                    value = rec[f]
                    if hasattr(value, 'name'):
                        value = value.name
                    row[f] = value
                data.append(row)
            result = {'list': data, 'fields': fields}
        else:
            result = None
        _logger.error(f"result: {result}")
        return result

    def _format_response(self, question, result, api_key):
        """Dùng Gemini để tạo câu trả lời tự nhiên từ kết quả"""
        if 'count' in result:
            prompt = f"Trả lời câu hỏi: {question}\nKết quả: Có {result['count']} bản ghi.\nHãy trả lời một câu ngắn gọn, lịch sự."
        elif 'list' in result:
            items = result['list']
            if not items:
                return "Không tìm thấy bản ghi nào."
            # Tạo danh sách đơn giản
            lines = []
            for item in items:
                line = ', '.join([f"{k}: {v}" for k, v in item.items()])
                lines.append(line)
            prompt = f"Trả lời câu hỏi: {question}\nKết quả: {lines}\nHãy trả lời một câu ngắn gọn, liệt kê theo danh sách."
        else:
            return "Xin lỗi, tôi chưa hiểu câu hỏi."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(url, json=data, headers=headers, timeout=300)
            if response.status_code != 200:
                return "Xin lỗi, có lỗi xảy ra."
            result = response.json()
            answer = result['candidates'][0]['content']['parts'][0]['text']
            return answer
        except:
            return "Xin lỗi, không thể tạo câu trả lời."

    def _fallback_response(self, question, api_key):
        """Khi không phân tích được intent, hỏi Gemini trực tiếp"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": f"Trả lời câu hỏi sau một cách lịch sự, nếu không biết thì nói rằng bạn chưa hiểu: {question}"}]}]}
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code != 200:
                return "Xin lỗi, có lỗi xảy ra."
            result = response.json()
            answer = result['candidates'][0]['content']['parts'][0]['text']
            return answer
        except:
            return "Xin lỗi, tôi chưa hiểu câu hỏi. Bạn có thể hỏi về số lượng nhân viên, dự án, công việc không?"