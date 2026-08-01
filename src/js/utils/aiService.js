/* ==========================================================================
   Google AI Studio / Gemini API Service Integration
   ========================================================================== */

/**
 * Smart AI Grocery Search & Recipe Suggestions powered by Google AI Studio
 * @param {string} userQuery Natural language query e.g. "What to cook for breakfast?"
 * @param {string} apiKey Google AI Studio API Key from .env
 */
export async function fetchAISmartSuggestions(userQuery, apiKey) {
  if (!apiKey || apiKey.includes('YOUR_GOOGLE_AI_STUDIO_API_KEY')) {
    return null;
  }

  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

  const promptText = `
You are the Blinkit Quick Commerce AI Shopping Assistant.
The user is searching for: "${userQuery}".
Suggest 3-4 specific grocery items or fresh ingredients available for 10-minute delivery.
Respond concisely in plain text bullet points.
`;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{
          parts: [{ text: promptText }]
        }]
      })
    });

    if (!response.ok) {
      console.warn('Google AI Studio API response status:', response.status);
      return null;
    }

    const data = await response.json();
    const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;
    return candidateText || null;
  } catch (error) {
    console.error('Failed to call Google AI Studio API:', error);
    return null;
  }
}
