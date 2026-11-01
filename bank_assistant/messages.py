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
    "om": {  # Afaan Oromoo
        "greeting": (
            "Akkam! 👋 Baankii Daashiniitti baga nagaan dhuftan. Ani gargaaraa keessan isa dijitaalaa dha. "
            "Har'a herrega Baankii Daashin akka banattan isin gargaara. Haa jalqabnu?"
        ),
        "greeting_deny": "Rakkoo hin qabu. Yeroo qophooftan \"eeyyee\" jedhaa, ni jalqabna.",
        "ask_full_name": "Baay'ee gaarii! Jalqaba, maaloo maqaa keessan guutuu natti himaa.",
        "ask_date_of_birth": "Galatoomaa, {first_name}. Itti aansee, guyyaan dhalootaa keessanii yoomi?",
        "ask_birth_city": "Itti aansee, maaloo magaalaa itti dhalattan natti himaa.",
        "ask_nationality": "Hubadheera. Lammummaan keessan maali?",
        "ask_account_type": (
            "Gosa herregaa kam banachuu barbaaddu? Qusannaa, Herrega Deddeebii (Current), "
            "Qusannaa Dhala Malee (Wadiah) moo Kuusaa Yeroo Murtaa'e?"
        ),
        "ask_fan": (
            "Amma, Eenyummaa Biyyaalessaatiin eenyummaa keessan haa mirkaneessinu. "
            "Maaloo lakkoofsa FAN keessanii (Lakkoofsa Eenyummaa Faydaa) galchaa."
        ),
        "otp_sent": (
            "Galatoomaa. Jecha icciitii yeroo tokkoo (OTP) lakkoofsa bilbilaa keessan kan Eenyummaa "
            "Biyyaalessaatti galmaa'e ({phone}) irratti ergineerra. Itti fufuuf galchaa."
        ),
        "otp_ok": "Eenyummaan keessan mirkanaa'eera. Maaloo odeeffannoo galmee Eenyummaa Biyyaalessaa irraa argame ilaalaa.",
        "otp_bad": "Koodiin sun sirrii miti. Maaloo irra deebi'aa yaalaa (yaaliin hafe: {left}).",
        "otp_expired": "Yeroon koodii sanaa darbeera. Haaraa argachuuf \"Irra deebi'ii ergi\" tuqaa.",
        "otp_locked": "Yaaliin dogoggoraa baay'ee ta'eera. Koodii haaraa gaafachuuf FAN keessan irra deebi'aa galchaa.",
        "otp_resent": "OTP haaraan gara {phone} ergameera.",
        "review_edit": "Rakkoo hin qabu. Odeeffannoo keessan haa sirreessinu. Gosa herregaa kam banachuu barbaaddu?",
        "creating": "Herregni keessan banamaa jira…",
        "done": "Baga gammaddan! Herregni Baankii Daashin keessanii amma hojii irra jira.",
        "err_name": "Dhiifama, maqaa keessan guutuu hin dhageenye. Maaloo maqaa keessanii fi maqaa abbaa keessanii natti himaa, fkn. \"Caalaa Tolaa Gammachuu\".",
        "err_dob": "Dhiifama, guyyaa sana hin hubanne. Maaloo guyyaa dhalootaa keessanii dubbadhaa ykn filadhaa, fkn. 15/01/2000.",
        "err_underage": "Herrega ofiin banachuuf umuriin keessan yoo xiqqaate waggaa {min_age} ta'uu qaba. Maaloo guyyaa sana mirkaneessaa, ykn eegduu wajjin damee daawwadhaa.",
        "err_city": "Dhiifama, magaalaa sana hin dhageenye. Magaalaa itti dhalattan natti himaa, fkn. \"Finfinnee\".",
        "err_nationality": "Dhiifama, hin hubanne. Lammummaan keessan maali? Fkn. \"Itoophiyaa\".",
        "err_account_type": "Maaloo tokko filadhaa: Qusannaa, Herrega Deddeebii, Qusannaa Dhala Malee (Wadiah) ykn Kuusaa Yeroo Murtaa'e.",
        "err_fan": "Lakkoofsi FAN (Lakkoofsa Eenyummaa Faydaa) dijiitii 12 qaba, fkn. 1234 5678 9012. Maaloo irra deebi'aa galchaa.",
        "fallback_question": "Herrega akka banattan isin gargaaruuf asan jira. Gaaffii bal'aa tajaajila irratti hojjetaan damee isin gargaaruu danda'a.",
        "invalid_state": "Yeroon keessan darbeera. Irra deebi'nee haa jalqabnu.",
    },
    "ti": {  # ትግርኛ
        "greeting": (
            "ሰላም! 👋 ናብ ዳሽን ባንክ እንቋዕ ብደሓን መጻእኩም። ኣነ ዲጂታላዊ ሓጋዚኹም እየ። "
            "ሎሚ ናይ ዳሽን ባንክ ሕሳብ ክትከፍቱ ክሕግዘኩም እየ። ንጀምር ዶ?"
        ),
        "greeting_deny": "ጸገም የብሉን። ምስ ተዳለኹም \"እወ\" በሉ፣ ክንጅምር ኢና።",
        "ask_full_name": "ጽቡቕ! መጀመርታ፣ በጃኹም ምሉእ ስምኩም ንገሩኒ።",
        "ask_date_of_birth": "የቐንየለይ {first_name}። ብምቕጻል፣ ዕለት ልደትኩም መዓስ እዩ?",
        "ask_birth_city": "ብምቕጻል፣ በጃኹም እተወለድኩምላ ከተማ ንገሩኒ።",
        "ask_nationality": "ተረዲኡኒ። ዜግነትኩም እንታይ እዩ?",
        "ask_account_type": "ኣየናይ ዓይነት ሕሳብ ክትከፍቱ ትደልዩ? ቁጠባ፣ ተንቀሳቓሲ፣ ብዘይ ወለድ (ዋዲዓ) ቁጠባ ወይ ናይ ግዜ ገደብ ተቐማጢ?",
        "ask_fan": "ሕጂ ብሃገራዊ መንነት መንነትኩም ነረጋግጽ። በጃኹም ቁጽሪ FAN ኩም (ቁጽሪ መንነት ፋይዳ) ኣእትዉ።",
        "otp_sent": "የቐንየለይ። ኣብ ሃገራዊ መንነት ናብ ዝተመዝገበ ቁጽሪ ስልኪኹም ({phone}) ናይ ሓደ ግዜ መሕለፊ ቃል (OTP) ልኢኽና ኣለና። ንምቕጻል ኣእትውዎ።",
        "otp_ok": "መንነትኩም ተረጋጊጹ ኣሎ። በጃኹም ካብ ሃገራዊ መንነት ዝተረኽበ ሓበሬታ ገምግሙ።",
        "otp_bad": "እቲ ኮድ ቅኑዕ ኣይኮነን። በጃኹም እንደገና ፈትኑ (ዝተረፉ ፈተነታት፦ {left})።",
        "otp_expired": "እቲ ኮድ ግዜኡ ሓሊፉ። ሓድሽ ንምርካብ \"ደጊምካ ስደድ\" ጠውቑ።",
        "otp_locked": "ብዙሕ ጌጋ ፈተነታት። ሓድሽ ኮድ ንምሕታት FAN ኩም ደጊምኩም ኣእትዉ።",
        "otp_resent": "ሓድሽ OTP ናብ {phone} ተላኢኹ ኣሎ።",
        "review_edit": "ጸገም የብሉን። ሓበሬታኹም ነስተኻኽል። ኣየናይ ዓይነት ሕሳብ ክትከፍቱ ትደልዩ?",
        "creating": "ሕሳብኩም ይኽፈት ኣሎ…",
        "done": "እንቋዕ ሓጎሰኩም! ናይ ዳሽን ባንክ ሕሳብኩም ሕጂ ንጡፍ እዩ።",
        "err_name": "ይቕሬታ፣ ምሉእ ስምኩም ኣይሰማዕኩን። በጃኹም ስምኩምን ስም ኣቦኹምን ንገሩኒ፣ ንኣብነት \"ሃብቶም ገብረመድህን ተስፋይ\"።",
        "err_dob": "ይቕሬታ፣ እቲ ዕለት ኣይተረደኣንን። በጃኹም ዕለት ልደትኩም ተዛረቡ ወይ ምረጹ (ንኣብነት 15/01/2000)።",
        "err_underage": "ብገዛእ ርእስኹም ሕሳብ ንምኽፋት እንተወሓደ {min_age} ዓመት ክትኮኑ ኣለኩም። በጃኹም ዕለቱ ኣረጋግጹ ወይ ምስ ሓላዊ ናብ ጨንፈር ኪዱ።",
        "err_city": "ይቕሬታ፣ እታ ከተማ ኣይሰማዕኩዋን። እተወለድኩምላ ከተማ ንገሩኒ፣ ንኣብነት \"መቐለ\"።",
        "err_nationality": "ይቕሬታ፣ ኣይተረደኣንን። ዜግነትኩም እንታይ እዩ? ንኣብነት \"ኢትዮጵያዊ\"።",
        "err_account_type": "በጃኹም ሓደ ምረጹ፦ ቁጠባ፣ ተንቀሳቓሲ፣ ብዘይ ወለድ (ዋዲዓ) ቁጠባ ወይ ናይ ግዜ ገደብ ተቐማጢ።",
        "err_fan": "ቁጽሪ FAN (ቁጽሪ መንነት ፋይዳ) 12 ኣሃዛት ኣለዎ፣ ንኣብነት 1234 5678 9012። በጃኹም ደጊምኩም ኣእትዉ።",
        "fallback_question": "ሕሳብ ንክትከፍቱ ክሕግዘኩም ኣብዚ ኣለኹ። ብዛዕባ ኣገልግሎታት ዝርዝር ሕቶታት ሰራሕተኛ ጨንፈር ክሕግዘኩም ይኽእል።",
        "invalid_state": "ግዜ ክፍለ-ግዜኹም ሓሊፉ። ደጊምና ንጀምር።",
    },
    "so": {  # Soomaali
        "greeting": (
            "Salaan! 👋 Ku soo dhawoow Bangiga Dashen. Waxaan ahay kaaliyahaaga dijitaalka ah. "
            "Maanta waxaan kaa caawinayaa inaad furato akoon Bangiga Dashen. Ma bilownaa?"
        ),
        "greeting_deny": "Dhib malahan. Markaad diyaar noqoto dheh \"haa\" waanan bilaabaynaa.",
        "ask_full_name": "Aad u fiican! Marka hore, fadlan ii sheeg magacaaga oo buuxa.",
        "ask_date_of_birth": "Mahadsanid, {first_name}. Marka xigta, waa maxay taariikhda dhalashadaadu?",
        "ask_birth_city": "Marka xigta, fadlan ii sheeg magaalada aad ku dhalatay.",
        "ask_nationality": "Waan fahmay. Waa maxay jinsiyaddaadu?",
        "ask_account_type": (
            "Nooca akoon ee aad rabto inaad furato? Kaydin, Akoon Socda (Current), "
            "Kaydin aan Ribo lahayn (Wadiah) mise Dhigaal Muddo Go'an?"
        ),
        "ask_fan": (
            "Hadda, aan ku xaqiijinno aqoonsigaaga Aqoonsiga Qaranka. "
            "Fadlan geli lambarkaaga FAN (Lambarka Aqoonsiga Fayda)."
        ),
        "otp_sent": (
            "Mahadsanid. Waxaan eray-sir hal mar ah (OTP) u dirnay lambarka taleefankaaga ee "
            "ku diiwaangashan Aqoonsiga Qaranka ({phone}). Fadlan geli si aad u sii wadato."
        ),
        "otp_ok": "Aqoonsigaaga waa la xaqiijiyay. Fadlan dib u eeg xogta laga helay diiwaanka Aqoonsiga Qaranka.",
        "otp_bad": "Koodhkaasi sax maaha. Fadlan isku day mar kale (isku dayada haray: {left}).",
        "otp_expired": "Koodhkaasi waqtigiisii wuu dhacay. Fadlan taabo \"Dib u dir\" si aad u hesho mid cusub.",
        "otp_locked": "Isku dayo khaldan oo badan. Fadlan dib u geli FAN-kaaga si aad u codsato kood cusub.",
        "otp_resent": "OTP cusub ayaa loo diray {phone}.",
        "review_edit": "Dhib malahan. Aan cusboonaysiinno xogtaada. Nooca akoon ee aad rabto inaad furato?",
        "creating": "Akoonkaaga waa la furayaa…",
        "done": "Hambalyo! Akoonkaaga Bangiga Dashen hadda waa firfircoon yahay.",
        "err_name": "Waan ka xumahay, ma maqlin magacaaga oo buuxa. Fadlan sheeg magacaaga iyo magaca aabbahaa, tusaale \"Cabdi Maxamed Cali\".",
        "err_dob": "Waan ka xumahay, ma fahmin taariikhdaas. Fadlan sheeg ama dooro taariikhda dhalashadaada, tusaale 15/01/2000.",
        "err_underage": "Waa inaad ugu yaraan {min_age} jir tahay si aad keligaa akoon u furato. Fadlan hubi taariikhda, ama laanta booqo adigoo la socda waalid/mas'uul.",
        "err_city": "Waan ka xumahay, ma maqlin magaalada. Fadlan ii sheeg magaalada aad ku dhalatay, tusaale \"Jigjiga\".",
        "err_nationality": "Waan ka xumahay, ma fahmin. Waa maxay jinsiyaddaadu? Tusaale \"Itoobiyaan\".",
        "err_account_type": "Fadlan dooro mid: Kaydin, Akoon Socda, Kaydin aan Ribo lahayn (Wadiah) ama Dhigaal Muddo Go'an.",
        "err_fan": "Lambarka FAN (Lambarka Aqoonsiga Fayda) wuxuu ka kooban yahay 12 tiro, tusaale 1234 5678 9012. Fadlan mar kale geli.",
        "fallback_question": "Waxaan halkan u joogaa inaan kaa caawiyo furashada akoonkaaga. Su'aalaha faahfaahsan ee adeegyada, shaqaalaha laanta ayaa kaa caawin kara.",
        "invalid_state": "Fadhigaagu wuu dhacay. Aan dib u bilowno.",
    },
    "aa": {  # Qafar af – draft, have a native speaker review before production
        "greeting": (
            "Nagaa! 👋 Dashen Baanki fan nagayat tamaateen. Anu ku dijitaal kaalitiyya. "
            "Asaaku Dashen Baanki akaawunti fakkaanam siinik kaalah. Qimbisnaa?"
        ),
        "greeting_deny": "Umaanéy mali. Qeedaaqtaanih \"ey\" iya, qimbisnay.",
        "ask_full_name": "Meqe! Awwaltah, ku migaq inkih yoh warisay.",
        "ask_date_of_birth": "Gadda ge, {first_name}. Tohuk lakal, ku dalwa ayro maay?",
        "ask_birth_city": "Tohuk lakal, ku dalteh magaala yoh warisay.",
        "ask_nationality": "Yoobbeh. Ku baaxo (zeginnet) maay?",
        "ask_account_type": "Ayi akaawunti fakkaanam faxxa? Savings, Current, Interest-Free (Wadiah) Savings hinnay Fixed Time Deposit?",
        "ask_fan": "Away, National ID (Fayda) ku agata xiinisna. Ku FAN lowo (Fayda ID Number) culusay.",
        "otp_sent": "Gadda ge. National ID addal ku taleefoon lowot ({phone}) inki-ruuq OTP ruubenno. Culusay.",
        "otp_ok": "Ku agata xiinisime. National ID addak beyneh mangaqo ablay.",
        "otp_bad": "Kood massa hinna. Qusbah gabbat (raaqe gabbatta: {left}).",
        "otp_expired": "Kood wakti tatre. Qusba kood ruubuh \"Resend\" tuqus.",
        "otp_locked": "Massa hinna gabbatta maggo. Qusba kood esseraanam FAN qusbah culusay.",
        "otp_resent": "Qusba OTP {phone} fan ruubime.",
        "review_edit": "Umaanéy mali. Ku mangaqo cusbisna. Ayi akaawunti fakkaanam faxxa?",
        "creating": "Ku akaawunti fakkeenimtaah tan…",
        "done": "Meqe! Ku Dashen Baanki akaawunti away taamitah tan.",
        "err_name": "Dambi ma lih, ku migaq inkih maabbem. Ku migaq kee ku abbah migaq yoh warisay.",
        "err_dob": "Dambi ma lih, ayro maaxiggem. Ku dalwa ayro warisay hinnay doorit (15/01/2000).",
        "err_underage": "Akaawunti fakkaanam {min_age} kalqaa kak dagoo hinnay ku edde faxxima. Ayro ablay, hinnay ku abbaah luk baanki fan amaatay.",
        "err_city": "Dambi ma lih, magaala maabbem. Ku dalteh magaala warisay, \"Samara\" ceelah.",
        "err_nationality": "Dambi ma lih, maaxiggem. Ku baaxo maay? \"Ethiopian\" ceelah.",
        "err_account_type": "Inki doorit: Savings, Current, Interest-Free (Wadiah) Savings hinnay Fixed Time Deposit.",
        "err_fan": "FAN (Fayda ID Number) 12 ixxima lih, 1234 5678 9012 ceelah. Qusbah culusay.",
        "fallback_question": "Akaawunti fakkaanam siinik kaalah anu akkel an. Baanki branch xaagi taamitu siinik kaalah duudah.",
        "invalid_state": "Wakti tatre. Qusbah qimbisna.",
    },
}

# Language codes the assistant supports, with the name used in LLM prompts.
LANGUAGES: dict[str, str] = {
    "en": "English",
    "am": "Amharic",
    "om": "Afaan Oromo",
    "ti": "Tigrinya",
    "so": "Somali",
    "aa": "Afar",
}

ACKS = {
    "en": ["Thank you.", "Great.", "Perfect."],
    "am": ["አመሰግናለሁ።", "በጣም ጥሩ።", "ጥሩ።"],
    "om": ["Galatoomaa.", "Baay'ee gaarii.", "Tole."],
    "ti": ["የቐንየለይ።", "ጽቡቕ።", "ሕራይ።"],
    "so": ["Mahadsanid.", "Aad u fiican.", "Waa hagaag."],
    "aa": ["Gadda ge.", "Meqe.", "Yoobbeh."],
}


def t(lang: str, key: str, **kwargs) -> str:
    table = MESSAGES.get(lang) or MESSAGES["en"]
    text = table.get(key) or MESSAGES["en"][key]
    return text.format(**kwargs) if kwargs else text
