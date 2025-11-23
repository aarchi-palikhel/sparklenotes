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
        if "summarize" in prompt.lower():
            summaries = [
                "✨ This note is so lovely! It talks about important things in a beautiful way. Keep writing your sparkly thoughts! 💖",
                "🌟 What a wonderful note! The main ideas are clear and inspiring. You're doing amazing, sweetie! 🎀",
                "💫 This note has such cute ideas! The key points shine through beautifully. Keep up the fantastic work! 🌈",
                "🎀 Your note is absolutely charming! The main thoughts shine through like little stars in the sky! ✨",
                "💕 Such beautiful writing! The essence of your note is clear and inspiring. You're a natural! 🌟"
            ]
            return random.choice(summaries)
        
        elif "suggest" in prompt.lower() or "task" in prompt.lower():
            suggestions = [
                "🎯 Here are some sparkly suggestions for your task:\n• Break it into smaller, cute steps\n• Set a fun timer for each part\n• Reward yourself with something sweet after! 🍬",
                "💡 Task ideas for you:\n• Gather all your supplies first\n• Create a cozy workspace\n• Play some happy music while working! 🎵",
                "🌟 Suggested steps:\n• Make a colorful checklist\n• Take cute breaks in between\n• Celebrate every little victory! 🎉",
                "✨ Sparkly plan:\n• Start with the most fun part first\n• Take pictures of your progress\n• Share your achievement with friends! 📸",
                "💫 Your task roadmap:\n• Prepare your materials\n• Set up a pretty workspace\n• Enjoy the process with a smile! 😊"
            ]
            return random.choice(suggestions)
        
        else:
            encouraging_messages = [
                "🤖 I'd love to help with that! For now, here's some encouragement: You're doing amazing and your notes are wonderful! 💕",
                "🌟 You're so creative! Keep up the fantastic work with your notes and tasks! ✨",
                "💫 Your dedication to organizing your thoughts is inspiring! Keep shining! 🌈",
                "🎀 Every note you write makes the world a little more organized and beautiful! 💖",
                "✨ Your productivity journey is going to be amazing! One step at a time! 🌟"
            ]
            return random.choice(encouraging_messages)
    
    def summarize_note(self, content):
        if len(content.strip()) < 10:
            return "📝 Note is too short to summarize! Add more content. 💕"
        prompt = f"""Please summarize this note in 2-3 cute, friendly sentences. 
        Keep it positive and encouraging! Make it sound like a friendly helper:
        
        {content}
        
        Cute summary:"""
        return self.generate_response(prompt)
    
    def suggest_todo(self, task_description):
        if len(task_description.strip()) < 3:
            return "🎯 Please describe your task a bit more! I'd love to help! ✨"
        prompt = f"""Based on this task: '{task_description}', suggest 2-3 related cute subtasks or preparation steps. 
        Make it friendly, encouraging, and use emojis:
        
        Sparkly task suggestions:"""
        return self.generate_response(prompt)

# Create a global instance
gemini_client = GeminiClient()