#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""邮件发送服务（基于 aiosmtplib，适配 backend_su 配置）"""
import aiosmtplib
import ssl
from email.mime.text import MIMEText

import certifi
from app.core.config import settings
from email.header import Header


class EmailService:
    """简单邮件发送服务"""

    def __init__(self):
        self.host = settings.MAIL_HOST
        self.port = settings.MAIL_PORT
        self.username = getattr(settings, "MAIL_USERNAME", "")
        self.password = getattr(settings, "MAIL_PASSWORD", "")
        self.mail_from = getattr(settings, "MAIL_FROM", self.username)
        self.mail_from_name = getattr(settings, "MAIL_FROM_NAME", settings.APP_NAME)
        self.ssl_verify = getattr(settings, "MAIL_SSL_VERIFY", True)
        self.enabled = bool(self.username and self.password)

    def _build_tls_context(self) -> ssl.SSLContext:
        """优先使用 certifi 证书链，必要时允许关闭校验。"""
        if self.ssl_verify:
            context = ssl.create_default_context(cafile=certifi.where())
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            return context

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    async def send_verification_code(self, to_email: str, code: str, purpose: str = "注册") -> bool:
        """发送验证码邮件"""
        if not self.enabled:
            # 未配置邮箱时，视为发送成功（开发环境）
            print(f"[开发模式] 将验证码 {code} 发送到 {to_email}（未配置邮箱，跳过实际发送）")
            return True

        subject = f"【{self.mail_from_name}】{purpose}验证码"
        description = "您正在进行账号验证操作，请使用以下验证码完成验证："
        content = f"""
        <html>
        <head><meta charset="UTF-8"></head>
        <body>
            <p>{description}</p>
            <p style="font-size: 24px; font-weight: bold;">{code}</p>
            <p>验证码有效期 {settings.VERIFICATION_CODE_EXPIRE} 秒，请尽快使用。</p>
        </body>
        </html>
        """

        try:
            # 与参考项目保持一致，使用 aiosmtplib 简化编码问题
            message = MIMEText(content, 'html', 'utf-8')
            message['From'] = self.mail_from
            message['To'] = to_email
            message['Subject'] = str(Header(subject, 'utf-8'))

            tls_context = self._build_tls_context()
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=True,
                tls_context=tls_context,
                sender=self.mail_from,
                recipients=[to_email],
                local_hostname="localhost",
            )
            return True
        except Exception as e:
            print(
                f"Email send error: {str(e)} | "
                f"host={self.host} port={self.port} ssl_verify={self.ssl_verify}"
            )
            return False


email_service = EmailService()
