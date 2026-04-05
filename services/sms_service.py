import hashlib
import time
import requests
import json
from config import load_config


class SMSService:
    @staticmethod
    def _create_headers(api_key, api_pwd):
        timestamp = int(time.time())
        s = f"{api_key}{api_pwd}{timestamp}"
        sign = hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()
        return {
            'Content-Type': 'application/json;charset=utf-8',
            'Sign': sign,
            'Timestamp': str(timestamp),
            'Api-Key': api_key
        }

    @staticmethod
    def send_sms(phone_number, message):
        config = load_config()
        sms_config = config.get("sms_api", {})

        if not sms_config.get("enabled", False):
            return False, "SMS non activé dans les paramètres"

        api_key = sms_config.get("api_key", "")
        api_pwd = sms_config.get("api_pwd", "")
        app_id = sms_config.get("app_id", "")
        base_url = sms_config.get("base_url", "https://api.onbuka.com/v3")
        sender_id = sms_config.get("sender_id", "HRFlow")

        if not all([api_key, api_pwd, app_id]):
            return False, "Configuration SMS incomplète"

        try:
            headers = SMSService._create_headers(api_key, api_pwd)
            url = f"{base_url}/sendSms"
            body = {
                "appId": app_id,
                "numbers": phone_number,
                "content": message,
                "senderId": sender_id
            }
            response = requests.post(url, json=body, headers=headers, timeout=10)
            if response.status_code == 200:
                result = json.loads(response.text)
                return True, result
            return False, f"Erreur HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def notify_task_assigned(employee_name, employee_phone, task_title):
        if not employee_phone:
            return False, "Pas de numéro de téléphone"

        message = f"HRFlow: Bonjour {employee_name}, une nouvelle tâche vous a été attribuée: {task_title}"
        return SMSService.send_sms(employee_phone, message)
