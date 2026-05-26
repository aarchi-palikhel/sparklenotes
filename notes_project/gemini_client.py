import google.generativeai as genai
import os
import time
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    def __init__(self):
        # Get API key from .env file
        self.api_key = os.getenv('GEMINI_API_KEY')
        print(f"🔑 API Key loaded: {self.api_key[:10]}..." if self.api_key else "❌ No API key found")
        
        if not self.api_key or self.api_key == 'your-gemini-api-key-here':
            print("❌ Please set up your Gemini API key in the .env file")
            self.model = None
            self.use_mock = True
            return
        
        try:
            genai.configure(api_key=self.api_key)
            
            # Try models that are less likely to be quota-limited
            models_to_try = [
                'models/gemini-2.0-flash-001',
                'models/gemini-2.0-flash-lite',
                'models/gemini-flash-latest',
                'models/gemma-3-4b-it',
                'models/gemini-2.5-flash',
            ]
            
            for model_name in models_to_try:
                try:
                    print(f"🔄 Trying model: {model_name}")
                    self.model = genai.GenerativeModel(model_name)
                    # Test with a very small prompt
                    test_response = self.model.generate_content("Hi")
                    print(f"✅ Connected with {model_name}! ✨")
                    self.current_model = model_name
                    self.use_mock = False
                    break
                except Exception as e:
                    if "quota" in str(e).lower() or "429" in str(e):
                        print(f"⏳ Quota exceeded for {model_name}, trying next...")
                        time.sleep(1)
                        continue
                    else:
                        print(f"❌ {model_name} failed: {e}")
                        continue
            else:
                print("💤 All models quota exceeded. Using mock responses.")
                self.model = None
                self.use_mock = True
                
        except Exception as e:
            print(f"❌ Configuration failed: {e}")
            self.model = None
            self.use_mock = True
    
    def generate_response(self, prompt):
        # If we don't have a working model, use mock responses
        if self.use_mock or self.model is None:
            return self._generate_mock_response(prompt)
        
        try:
            print(f"🤖 Sending to {self.current_model}: {prompt[:30]}...")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "quota" in str(e).lower() or "429" in str(e):
                print("💤 Quota exceeded, using mock response")
                return self._generate_mock_response(prompt)
            else:
                print(f"❌ API Error: {e}")
                return self._generate_mock_response(prompt)
    
    def _generate_mock_response(self, prompt):
        """Generate cute mock responses when quota is exceeded"""
        p = prompt.lower()
        if "summarize" in p:
            return random.choice([
                "✨ This note is so lovely! It talks about important things in a beautiful way. Keep writing your sparkly thoughts! 💖",
                "🌟 What a wonderful note! The main ideas are clear and inspiring. You're doing amazing, sweetie! 🎀",
                "💫 This note has such cute ideas! The key points shine through beautifully. Keep up the fantastic work! 🌈",
            ])
        elif "improve" in p or "rewrite" in p:
            return random.choice([
                "✨ Your note is already wonderful! Here's a polished version: This note captures key ideas clearly and concisely, making it easy to revisit and act upon. 💖",
                "🌟 Improved version: The main points are well-organized and presented in a clear, professional manner. Great work! 🎀",
            ])
        elif "title" in p:
            return random.choice([
                "✨ Sparkly Thoughts & Ideas",
                "💡 My Important Notes",
                "🌟 Key Insights & Reflections",
                "📝 Thoughts Worth Keeping",
            ])
        elif "mood" in p or "tone" in p or "emotion" in p:
            return random.choice(["focused 🎯", "happy 😊", "productive 💪", "calm 😌", "motivated 🌟"])
        elif "due date" in p or "deadline" in p or "when" in p:
            from datetime import datetime, timedelta
            suggested = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%dT09:00")
            return suggested
        elif "suggest" in p or "task" in p:
            return random.choice([
                "🎯 Break it into smaller steps\n• Set a fun timer\n• Reward yourself after! 🍬",
                "💡 Gather supplies first\n• Create a cozy workspace\n• Play happy music! 🎵",
            ])
        elif "digest" in p or "weekly" in p:
            return "✨ You had a productive week! Keep up the amazing work and stay sparkly! 💖"
        else:
            return random.choice([
                "🤖 You're doing amazing and your notes are wonderful! 💕",
                "🌟 Keep up the fantastic work with your notes and tasks! ✨",
            ])

    # ── Existing methods ───────────────────────────────────────────────────────

    def summarize_note(self, content):
        if len(content.strip()) < 10:
            return "📝 Note is too short to summarize! Add more content. 💕"
        prompt = f"""Please summarize this note in 2-3 cute, friendly sentences.
Keep it positive and encouraging:

{content}

Cute summary:"""
        return self.generate_response(prompt)

    def suggest_todo(self, task_description):
        if len(task_description.strip()) < 3:
            return "🎯 Please describe your task a bit more! I'd love to help! ✨"
        prompt = f"""Based on this task: '{task_description}', suggest 2-3 related subtasks or preparation steps.
Make it friendly, encouraging, and use emojis:

Sparkly task suggestions:"""
        return self.generate_response(prompt)

    # ── New AI methods ─────────────────────────────────────────────────────────

    def improve_note(self, content, style='clear'):
        """Rewrite a note to be clearer or more formal."""
        if len(content.strip()) < 10:
            return "📝 Note is too short to improve! Add more content first. 💕"
        style_instruction = (
            "more formal and professional" if style == 'formal'
            else "clearer, more concise, and easier to read"
        )
        prompt = f"""Please rewrite the following note to be {style_instruction}.
Keep all the original information but improve the writing quality.
Return only the rewritten note, no extra commentary:

{content}

Improved version:"""
        return self.generate_response(prompt)

    def suggest_title(self, content):
        """Auto-suggest a short title based on note content."""
        if len(content.strip()) < 10:
            return "My Note"
        prompt = f"""Based on this note content, suggest a short, catchy title (5-8 words max).
Return only the title, nothing else:

{content}

Title:"""
        result = self.generate_response(prompt)
        # Strip quotes and extra whitespace Gemini sometimes adds
        return result.strip().strip('"').strip("'").strip()

    def detect_mood(self, content):
        """Detect the emotional tone of a note."""
        if len(content.strip()) < 5:
            return "neutral 😐"
        prompt = f"""Analyze the emotional tone of this text and respond with exactly one word
describing the mood, followed by a single matching emoji.
Examples: "stressed 😰", "happy 😊", "focused 🎯", "sad 😢", "excited 🎉", "calm 😌", "motivated 💪"

Text: {content}

Mood (one word + emoji):"""
        result = self.generate_response(prompt)
        return result.strip().split('\n')[0].strip()

    def suggest_due_date(self, task_description):
        """Suggest a realistic due date/time for a task."""
        if len(task_description.strip()) < 3:
            return None
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        prompt = f"""Today is {today}. Based on this task description, suggest a realistic due date and time.
Reply with ONLY a datetime in this exact format: YYYY-MM-DDTHH:MM
No explanation, no extra text, just the datetime string.

Task: {task_description}

Due datetime:"""
        result = self.generate_response(prompt).strip()
        # Validate the format before returning
        try:
            datetime.strptime(result[:16], "%Y-%m-%dT%H:%M")
            return result[:16]
        except ValueError:
            return None

    def generate_weekly_digest(self, user, notes, completed_todos, pending_todos):
        """Generate a personalised weekly digest summary."""
        notes_text = "\n".join([f"- {n.title}: {n.content[:80]}..." for n in notes[:5]]) or "No notes this week."
        completed_text = "\n".join([f"- {t.title}" for t in completed_todos[:10]]) or "No completed tasks."
        pending_text = "\n".join([f"- {t.title}" for t in pending_todos[:5]]) or "No pending tasks."

        prompt = f"""Write a warm, encouraging weekly digest for {user.username}.
Keep it to 3-4 sentences. Be positive and motivating.

This week's notes:
{notes_text}

Completed tasks:
{completed_text}

Still pending:
{pending_text}

Weekly digest message:"""
        return self.generate_response(prompt)


# Create a global instance
gemini_client = GeminiClient()