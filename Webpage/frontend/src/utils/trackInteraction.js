import api from '../api/tokenHandler';

const SESSION_TIMEOUT_MINUTES = 30 * 60 * 1000; // 30 minut w milisekundach

export const getSessionId = () => {
  let session_data = JSON.parse(localStorage.getItem('session'));
  const now = Date.now();

    if (session_data && (now - session_data.lastActivity < SESSION_TIMEOUT_MINUTES)) { 
        session_data.lastActivity = now;
        localStorage.setItem('session', JSON.stringify(session_data));
        return session_data.id;
    }

    const newSessionId = crypto.randomUUID();
    session_data = {
        id: newSessionId,
        lastActivity: now
    };
    localStorage.setItem('session', JSON.stringify(session_data));
    return newSessionId;
};

export const clearSessionId = () => {
  localStorage.removeItem('session');
};

export const trackInteraction = async (productId, type) => {
  try {
        await api.post('/analytics/user-product-interactions', {
        product_id: productId,
        type: type,
        session_id: getSessionId()
        });
  } catch (err) {
    console.error(err);
  }
};
