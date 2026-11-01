"""Bilingual (English / Amharic) script for the AI assistant."""
from __future__ import annotations

MESSAGES: dict[str, dict[str, str]] = {
    "en": {
        "greeting": (
            "Selam! 👋 Welcome to Dashen Bank. I'm your virtual assistant. "
            "I'll help you open a Dashen Bank account today. Shall we get started?"
        ),
        "greeting_deny": "No problem. Whenever you're ready, just say \"yes\" and we'll begin.",
        "ask_full_name": "Great! First, please tell me your full name.",
        "ask_date_of_birth": "Thank you, {first_name}. Next, what is your date of birth?",
        "ask_birth_city": "Next, please tell me the city where you were born.",
        "ask_nationality": "Got it. What is your nationality?",
        "ask_account_type": (
            "Which type of account would you like to open? "
            "Savings, Current, Interest-Free (Wadiah) Savings or Fixed Time Deposit?"
        ),
        "ask_fan": (
            "Now, let's verify your identity using your National ID. "
            "Please enter your FAN number (Fayda ID Number)."
        ),
        "otp_sent": (
            "Thank you. I've sent a one-time password (OTP) to your mobile number "
            "registered with National ID ({phone}). Please enter it to continue."
        ),
        "otp_ok": "Your identity is verified. Please review the details we retrieved from the National ID database.",
        "otp_bad": "That code is not correct. Please try again ({left} attempt(s) left).",
        "otp_expired": "That code has expired. Please tap \"Resend\" to get a new one.",
        "otp_locked": "Too many incorrect attempts. Please re-enter your FAN to request a new code.",
        "otp_resent": "A new OTP has been sent to {phone}.",
        "review_edit": "No problem. Let's update your details. Which type of account would you like to open?",
        "creating": "Creating your account…",
        "done": "Congratulations! Your Dashen Bank account is now active.",
        "err_name": "Sorry, I didn't catch your full name. Please say your first name and father's name, for example \"Betelhem Tesfaye Alemu\".",
        "err_dob": "Sorry, I couldn't understand that date. Please say or select your date of birth, for example \"Jan 15, 2000\".",
        "err_underage": "You need to be at least {min_age} years old to open an account on your own. Please check the date of birth, or visit a branch to open a minor's account with a guardian.",
        "err_city": "Sorry, I didn't catch the city. Please tell me the city where you were born, for example \"Addis Ababa\".",
        "err_nationality": "Sorry, I didn't catch that. What is your nationality? For example \"Ethiopian\".",
        "err_account_type": "Please choose one of: Savings, Current, Interest-Free (Wadiah) Savings or Fixed Time Deposit.",
        "err_fan": "A FAN (Fayda ID Number) has 12 digits, for example 1234 5678 9012. Please enter it again.",
        "fallback_question": "I'm here to help you open your account. A branch officer can answer detailed product questions.",
        "invalid_state": "Your session has expired. Let's start again.",
    },
    "am": {
        "greeting": (
            "ሰላም! 👋 ወደ ዳሽን ባንክ እንኳን በደህና መጡ። እኔ የእርስዎ ምናባዊ ረዳት ነኝ። "
            "ዛሬ የዳሽን ባንክ ሂሳብ እንዲከፍቱ እረዳዎታለሁ። እንጀምር?"
        ),
        "greeting_deny": "ችግር የለም። ዝግጁ ሲሆኑ \"አዎ\" ይበሉ እና እንጀምራለን።",
        "ask_full_name": "በጣም ጥሩ! በመጀመሪያ እባክዎ ሙሉ ስምዎን ይንገሩኝ።",
        "ask_date_of_birth": "አመሰግናለሁ {first_name}። በመቀጠል የትውልድ ቀንዎ መቼ ነው?",
        "ask_birth_city": "በመቀጠል እባክዎ የተወለዱበትን ከተማ ይንገሩኝ።",
        "ask_nationality": "ገባኝ። ዜግነትዎ ምንድን ነው?",
        "ask_account_type": "የትኛውን የሂሳብ አይነት መክፈት ይፈልጋሉ? ቁጠባ፣ ተንቀሳቃሽ፣ ከወለድ ነፃ (ወዲአህ) ቁጠባ ወይስ የጊዜ ገደብ ተቀማጭ?",
        "ask_fan": "አሁን ማንነትዎን በብሔራዊ መታወቂያ እናረጋግጥ። እባክዎ የFAN ቁጥርዎን (የፋይዳ መታወቂያ ቁጥር) ያስገቡ።",
        "otp_sent": "አመሰግናለሁ። በብሔራዊ መታወቂያ ወደተመዘገበው ስልክ ቁጥርዎ ({phone}) የአንድ ጊዜ የይለፍ ቃል (OTP) ልከናል። ለመቀጠል ያስገቡት።",
        "otp_ok": "ማንነትዎ ተረጋግጧል። እባክዎ ከብሔራዊ መታወቂያ የተገኘውን መረጃ ይገምግሙ።",
        "otp_bad": "ኮዱ ትክክል አይደለም። እባክዎ እንደገና ይሞክሩ (የቀሩ ሙከራዎች፦ {left})።",
        "otp_expired": "ኮዱ ጊዜው አልፎበታል። አዲስ ለማግኘት \"እንደገና ላክ\" ይጫኑ።",
        "otp_locked": "በጣም ብዙ የተሳሳቱ ሙከራዎች። አዲስ ኮድ ለመጠየቅ FAN ቁጥርዎን እንደገና ያስገቡ።",
        "otp_resent": "አዲስ OTP ወደ {phone} ተልኳል።",
        "review_edit": "ችግር የለም። መረጃዎን እናስተካክል። የትኛውን የሂሳብ አይነት መክፈት ይፈልጋሉ?",
        "creating": "ሂሳብዎ እየተከፈተ ነው…",
        "done": "እንኳን ደስ አለዎት! የዳሽን ባንክ ሂሳብዎ አሁን ንቁ ነው።",
        "err_name": "ይቅርታ፣ ሙሉ ስምዎን አልሰማሁም። እባክዎ ስምዎን እና የአባትዎን ስም ይንገሩኝ።",
        "err_dob": "ይቅርታ፣ ቀኑን አልተረዳሁም። እባክዎ የትውልድ ቀንዎን ይናገሩ ወይም ይምረጡ (ለምሳሌ 15/01/2000)።",
        "err_underage": "በራስዎ ሂሳብ ለመክፈት ቢያንስ {min_age} ዓመት መሆን አለብዎት። እባክዎ ቀኑን ያረጋግጡ ወይም ከአሳዳጊ ጋር ቅርንጫፍ ይጎብኙ።",
        "err_city": "ይቅርታ፣ ከተማውን አልሰማሁም። የተወለዱበትን ከተማ ይንገሩኝ፣ ለምሳሌ \"አዲስ አበባ\"።",
        "err_nationality": "ይቅርታ፣ አልገባኝም። ዜግነትዎ ምንድን ነው? ለምሳሌ \"ኢትዮጵያዊ\"።",
        "err_account_type": "እባክዎ ይምረጡ፦ ቁጠባ፣ ተንቀሳቃሽ፣ ከወለድ ነፃ (ወዲአህ) ቁጠባ ወይም የጊዜ ገደብ ተቀማጭ።",
        "err_fan": "የFAN ቁጥር (የፋይዳ መታወቂያ ቁጥር) 12 አሃዞች አሉት፣ ለምሳሌ 1234 5678 9012። እባክዎ እንደገና ያስገቡ።",
        "fallback_question": "ሂሳብ እንዲከፍቱ ልረዳዎ እዚህ ነኝ። ስለ ምርቶች ዝርዝር ጥያቄዎች የቅርንጫፍ ሰራተኛ ሊረዳዎ ይችላል።",
        "invalid_state": "ክፍለ ጊዜዎ አልፎበታል። እንደገና እንጀምር።",
    },
}

ACKS = {"en": ["Thank you.", "Great.", "Perfect."], "am": ["አመሰግናለሁ።", "በጣም ጥሩ።", "ጥሩ።"]}


def t(lang: str, key: str, **kwargs) -> str:
    table = MESSAGES.get(lang) or MESSAGES["en"]
    text = table.get(key) or MESSAGES["en"][key]
    return text.format(**kwargs) if kwargs else text
