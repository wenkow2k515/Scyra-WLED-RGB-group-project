# AI Mood Feedback Feature

The Scyra app includes an AI-powered mood feedback feature that analyzes user mood survey responses and provides personalized feedback along with color recommendations.

## How It Works

1. Users complete a mood survey with metrics for energy, happiness, stress, anxiety, creativity, etc.
2. The system processes this data to generate:
   - Personalized text feedback based on the user's mood state
   - A color recommendation scientifically aligned with their emotional state
   - RGB values for the recommended color to control the lighting

## Dual Implementation

The mood feedback system works in two modes:

### 1. OpenAI API Mode (Recommended)

When an OpenAI API key is configured, the system uses the GPT-3.5-turbo model to generate highly personalized feedback and color recommendations. This provides the best user experience with:

- More nuanced understanding of mood combinations
- Consideration of journal text entries
- Human-like, empathetic responses
- Highly tailored color recommendations

**Configuration**: Add your OpenAI API key to your `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

### 2. Rule-Based Fallback Mode

If no OpenAI API key is available, the system automatically falls back to a rule-based algorithm that:

- Analyzes the numerical mood metrics
- Applies predefined rules to determine the appropriate feedback
- Selects colors based on psychological color theory
- Provides consistent, helpful responses without requiring an API

This ensures the app remains fully functional even without API access.

## Why GPT-3.5-turbo?

We use GPT-3.5-turbo rather than GPT-4 because:

1. **Wider availability**: More users have access to GPT-3.5-turbo
2. **Cost efficiency**: GPT-3.5-turbo is approximately 60x cheaper for inputs and 40x cheaper for outputs
3. **Faster responses**: Better user experience with quicker feedback generation
4. **Sufficient capabilities**: For our mood feedback use case, GPT-3.5-turbo provides excellent results

## Testing the Feature

You can test both modes using the provided test script:

```bash
python test_mood_utils.py
```

This script will:
1. Test with your configured API key if available
2. Demonstrate the fallback behavior by temporarily disabling the API key

## Customizing the Rules

The rule-based algorithm can be customized by editing the `generate_rule_based_feedback()` function in `app/mood_utils.py`. You can add new rules, adjust thresholds, or modify the feedback text to suit your specific needs. 