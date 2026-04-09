#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""通用辅助函数"""
import random
import string


def generate_verification_code(length: int = 6) -> str:
    """生成数字验证码"""
    return ''.join(random.choices(string.digits, k=length))
