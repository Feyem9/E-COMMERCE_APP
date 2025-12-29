export const environment = {
    production: true,
    apiUrl: 'https://theck-market.onrender.com',
    payUnit: {
        x_api_key: 'ta_clef_prod',
        authorization: 'Bearer ton_token_prod',
        baseUrl: 'https://api.payunit.net/api', // mode production
    },
    // 📊 Google Analytics
    analytics: {
        enabled: true,
        measurementId: 'G-F7ID8RRCXM'  // ✅ Measurement ID configuré
    }
};
