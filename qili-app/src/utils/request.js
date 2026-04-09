export const request = async (url, options = {}) => {
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  const token = localStorage.getItem('access_token');
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  const isFormData = options.body instanceof FormData;
  if (isFormData) {
    delete defaultHeaders['Content-Type']; // Let browser set boundary
  }

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  const baseURL = import.meta.env.VITE_API_BASE_URL || '';
  const fullUrl = url.startsWith('http') ? url : `${baseURL}${url}`;

  try {
    const response = await fetch(fullUrl, config);
    const data = await response.json();

    if (!response.ok) {
      const errorMessage = data.detail || data.message || '请求失败';
      throw new Error(errorMessage);
    }

    return data;
  } catch (error) {
    console.error(`Request to ${url} failed:`, error);
    throw error;
  }
};

export const get = (url, params = {}) => {
  const queryString = new URLSearchParams(params).toString();
  const finalUrl = queryString ? `${url}?${queryString}` : url;
  return request(finalUrl, { method: 'GET' });
};

export const post = (url, data, options = {}) => {
  const isFormData = data instanceof FormData;
  return request(url, {
    method: 'POST',
    body: isFormData ? data : JSON.stringify(data),
    ...options,
  });
};

export const put = (url, data, options = {}) => {
  const isFormData = data instanceof FormData;
  return request(url, {
    method: 'PUT',
    body: isFormData ? data : JSON.stringify(data),
    ...options,
  });
};

export const del = (url, options = {}) => {
  return request(url, { method: 'DELETE', ...options });
};
