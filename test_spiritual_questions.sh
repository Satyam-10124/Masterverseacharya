#!/bin/bash

# Comprehensive Test Script for MasterversAcharya API
# This script sends 150 diverse spiritual and religious questions to test the agent
# Questions cover multiple religions, difficulty levels, and theological concepts

# Color definitions
RESET="\033[0m"
BOLD="\033[1m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
WHITE="\033[37m"
BG_BLUE="\033[44m"
BG_GREEN="\033[42m"
BG_YELLOW="\033[43m"

# Configuration
API_URL="http://127.0.0.1:9876"
APP_NAME="masterversacharya"
USER_ID="test_user"
OUTPUT_FILE="spiritual_responses_comprehensive.csv"
SESSION_ID=""
QUESTION_COUNT=0

# Check if API server is running
echo -e "${CYAN}${BOLD}Checking if API server is running...${RESET}"
if ! curl -s "$API_URL/list-apps" > /dev/null; then
    echo -e "${RED}${BOLD}Error: API server is not running. Please start it with 'adk api_server' first.${RESET}"
    exit 1
fi

# Create a new session
echo -e "${CYAN}${BOLD}Creating a new session...${RESET}"
SESSION_RESPONSE=$(curl -s -X POST "$API_URL/apps/$APP_NAME/users/$USER_ID/sessions" \
    -H "Content-Type: application/json" \
    -d '{"state": {}}')

# Extract session ID
SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$SESSION_ID" ]; then
    echo -e "${RED}${BOLD}Error: Failed to create session.${RESET}"
    exit 1
fi

echo -e "${GREEN}${BOLD}Session created with ID: ${RESET}${YELLOW}$SESSION_ID${RESET}"

# Create CSV header
echo "Number,Category,Query,Response" > "$OUTPUT_FILE"

# Function to send a query and save the response
send_query() {
    local category="$1"
    local query="$2"
    QUESTION_COUNT=$((QUESTION_COUNT + 1))
    
    echo -e "${BLUE}[${QUESTION_COUNT}/150] ${YELLOW}[$category] ${RESET}${MAGENTA}\"$query\"${RESET}"
    
    # Call the API
    response=$(curl -s -X POST "$API_URL/run" \
        -H "Content-Type: application/json" \
        -d "{
            \"app_name\": \"$APP_NAME\",
            \"user_id\": \"$USER_ID\",
            \"session_id\": \"$SESSION_ID\",
            \"new_message\": {
                \"role\": \"user\",
                \"parts\": [{
                    \"text\": \"$query\"
                }]
            }
        }")
    
    # Extract the text response
    text_response=""
    
    # Try standard format first
    if echo "$response" | grep -q "candidates"; then
        text_response=$(echo "$response" | grep -o '"text":"[^"]*"' | head -1 | cut -d'"' -f4)
    fi
    
    # Try alternate format
    if [ -z "$text_response" ] && echo "$response" | grep -q "content"; then
        text_response=$(echo "$response" | grep -o '"text":"[^"]*"' | head -1 | cut -d'"' -f4)
    fi
    
    # Final fallback
    if [ -z "$text_response" ]; then
        text_response="[Error: Could not parse response]"
        echo -e "${RED}Failed to parse response${RESET}"
    else
        echo -e "${GREEN}✓ Response received${RESET}"
    fi
    
    # Escape quotes and commas for CSV format
    category_escaped=$(echo "$category" | sed 's/"/""/g')
    query_escaped=$(echo "$query" | sed 's/"/""/g')
    response_escaped=$(echo "$text_response" | sed 's/"/""/g')
    
    # Append to CSV
    echo "\"$QUESTION_COUNT\",\"$category_escaped\",\"$query_escaped\",\"$response_escaped\"" >> "$OUTPUT_FILE"
    
    # Wait between queries
    sleep 1.5
}

# Start testing
echo -e "\n${BG_BLUE}${WHITE}${BOLD} Starting Comprehensive Religious Knowledge Test - 150 Questions ${RESET}\n"

# SECTION 1: Basic Factual Questions (30 questions)
echo -e "\n${BG_GREEN}${WHITE}${BOLD} SECTION 1: Basic Factual Questions ${RESET}"

# Christianity (10)
send_query "Christianity-Basic" "What are the four Gospels in the New Testament?"
send_query "Christianity-Basic" "How many apostles did Jesus have?"
send_query "Christianity-Basic" "What is the first book of the Bible?"
send_query "Christianity-Basic" "Who baptized Jesus?"
send_query "Christianity-Basic" "What is the holy day of worship for Christians?"
send_query "Christianity-Basic" "What is the symbol of Christianity?"
send_query "Christianity-Basic" "Where was Jesus born?"
send_query "Christianity-Basic" "What is the Christian holy book called?"
send_query "Christianity-Basic" "How many commandments did Moses receive?"
send_query "Christianity-Basic" "What is the Trinity in Christianity?"

# Islam (10)
send_query "Islam-Basic" "What are the five pillars of Islam?"
send_query "Islam-Basic" "What is the holy book of Islam?"
send_query "Islam-Basic" "Who is the prophet of Islam?"
send_query "Islam-Basic" "What direction do Muslims face when praying?"
send_query "Islam-Basic" "What is the holy month of fasting called?"
send_query "Islam-Basic" "How many times a day do Muslims pray?"
send_query "Islam-Basic" "What is the Islamic declaration of faith called?"
send_query "Islam-Basic" "What are the two main branches of Islam?"
send_query "Islam-Basic" "What is the pilgrimage to Mecca called?"
send_query "Islam-Basic" "What does 'Allah' mean?"

# Hinduism (10)
send_query "Hinduism-Basic" "What are the four Vedas?"
send_query "Hinduism-Basic" "Who are the three gods in the Trimurti?"
send_query "Hinduism-Basic" "What is the Hindu festival of lights called?"
send_query "Hinduism-Basic" "What is the sacred river in Hinduism?"
send_query "Hinduism-Basic" "What is karma?"
send_query "Hinduism-Basic" "What is the Hindu symbol Om represent?"
send_query "Hinduism-Basic" "What are the four stages of life in Hinduism?"
send_query "Hinduism-Basic" "What is dharma?"
send_query "Hinduism-Basic" "What is the Hindu concept of rebirth called?"
send_query "Hinduism-Basic" "What is moksha?"

# SECTION 2: Buddhism & Eastern Religions (20 questions)
echo -e "\n${BG_GREEN}${WHITE}${BOLD} SECTION 2: Buddhism & Eastern Religions ${RESET}"

# Buddhism (10)
send_query "Buddhism" "What are the Four Noble Truths?"
send_query "Buddhism" "Who founded Buddhism?"
send_query "Buddhism" "What is the Middle Way?"
send_query "Buddhism" "What is Nirvana?"
send_query "Buddhism" "What are the Three Jewels of Buddhism?"
send_query "Buddhism" "What is the Buddhist concept of suffering called?"
send_query "Buddhism" "What is a Bodhisattva?"
send_query "Buddhism" "What are the main branches of Buddhism?"
send_query "Buddhism" "What is the Buddhist scripture called?"
send_query "Buddhism" "What does Buddha mean?"

# Other Eastern Religions (10)
send_query "Sikhism" "Who founded Sikhism?"
send_query "Sikhism" "What are the five Ks of Sikhism?"
send_query "Sikhism" "What is the Sikh holy book?"
send_query "Sikhism" "What is a gurdwara?"
send_query "Jainism" "What is ahimsa in Jainism?"
send_query "Jainism" "Who founded Jainism?"
send_query "Jainism" "What are the five vows of Jainism?"
send_query "Taoism" "What is the Tao?"
send_query "Taoism" "Who wrote the Tao Te Ching?"
send_query "Shinto" "What is kami in Shinto?"

# SECTION 3: Abrahamic Religions Deep Dive (20 questions)
echo -e "\n${BG_GREEN}${WHITE}${BOLD} SECTION 3: Abrahamic Religions Deep Dive ${RESET}"

# Judaism (10)
send_query "Judaism" "What is the Torah?"
send_query "Judaism" "What is the Sabbath in Judaism?"
send_query "Judaism" "What is a Bar/Bat Mitzvah?"
send_query "Judaism" "What are the main Jewish holidays?"
send_query "Judaism" "What is kosher food?"
send_query "Judaism" "What is the Talmud?"
send_query "Judaism" "Who was Abraham?"
send_query "Judaism" "What is the Star of David?"
send_query "Judaism" "What is Passover?"
send_query "Judaism" "What is a synagogue?"

# Comparative Abrahamic (10)
send_query "Comparative" "How are Abraham's sons important to Judaism, Christianity, and Islam?"
send_query "Comparative" "What do Jews, Christians, and Muslims believe about Jesus?"
send_query "Comparative" "How do the three Abrahamic faiths view Moses?"
send_query "Comparative" "What is the concept of monotheism in Abrahamic religions?"
send_query "Comparative" "How do dietary laws differ between Judaism and Islam?"
send_query "Comparative" "What is the role of Jerusalem in the three faiths?"
send_query "Comparative" "How do the concepts of heaven and hell differ?"
send_query "Comparative" "What prophets are shared between these religions?"
send_query "Comparative" "How do prayer practices differ?"
send_query "Comparative" "What is the concept of revelation in each faith?"

# SECTION 4: Scripture and Texts (20 questions)
echo -e "\n${BG_GREEN}${WHITE}${BOLD} SECTION 4: Scripture and Sacred Texts ${RESET}"

send_query "Scripture" "What language was the Bible originally written in?"
send_query "Scripture" "How many surahs are in the Quran?"
send_query "Scripture" "What is the Bhagavad Gita about?"
send_query "Scripture" "What are the Upanishads?"
send_query "Scripture" "What is the difference between the Hebrew Bible and the Old Testament?"
send_query "Scripture" "What are hadith in Islam?"
send_query "Scripture" "What is the Pali Canon?"
send_query "Scripture" "What are the Puranas?"
send_query "Scripture" "What is the Book of Mormon?"
send_query "Scripture" "What are the Dead Sea Scrolls?"
send_query "Scripture" "What is the Guru Granth Sahib?"
send_query "Scripture" "What are the Psalms?"
send_query "Scripture" "What is the I Ching?"
send_query "Scripture" "What are the Vedic hymns?"
send_query "Scripture" "What is the Avesta in Zoroastrianism?"
send_query "Scripture" "What are the Apocrypha?"
send_query "Scripture" "What is the Mahabharata?"
send_query "Scripture" "What are the Sutras in Buddhism?"
send_query "Scripture" "What is the Book of Revelation about?"
send_query "Scripture" "What are the Jataka tales?"

# SECTION 5: Practices and Rituals (20 questions)
echo -e "\n${BG_GREEN}${WHITE}${BOLD} SECTION 5: Practices and Rituals ${RESET}"

send_query "Practices" "What is baptism and which religions practice it?"
send_query "Practices" "What is meditation in different religions?"
send_query "Practices" "What are prayer beads used for?"
send_query "Practices" "What is fasting in different religions?"
send_query "Practices" "What is pilgrimage in various faiths?"
send_query "Practices" "What is confession in Christianity?"
send_query "Practices" "What is puja in Hinduism?"
send_query "Practices" "What is wudu in Islam?"
send_query "Practices" "What are mantras?"
send_query "Practices" "What is communion in Christianity?"
send_query "Practices" "What is circumcision in Abrahamic religions?"
send_query "Practices" "What are Hindu samskaras?"
send_query "Practices" "What is zazen in Zen Buddhism?"
send_query "Practices" "What is the Islamic call to prayer?"
send_query "Practices" "What are Jewish dietary laws?"
send_query "Practices" "What is yoga's religious significance?"
send_query "Practices" "What is the significance of incense in worship?"
send_query "Practices" "What are religious vows?"
send_query "Practices" "What is tithing?"
send_query "Practices" "What is the role of music in worship?"

# SECTION 6: Philosophical and Theological Questions (20 questions)
echo -e "\n${BG_YELLOW}${WHITE}${BOLD} SECTION 6: Philosophical and Theological Questions ${RESET}"

send_query "Philosophy" "What is the problem of evil in theology?"
send_query "Philosophy" "How do religions explain free will?"
send_query "Philosophy" "What is religious pluralism?"
send_query "Philosophy" "What is the difference between spirituality and religion?"
send_query "Philosophy" "How do religions view the soul?"
send_query "Philosophy" "What is mysticism in religion?"
send_query "Philosophy" "What is the concept of divine justice?"
send_query "Philosophy" "How do religions explain suffering?"
send_query "Philosophy" "What is religious experience?"
send_query "Philosophy" "What is the relationship between faith and reason?"
send_query "Philosophy" "What is natural theology?"
send_query "Philosophy" "How do religions view miracles?"
send_query "Philosophy" "What is religious ethics?"
send_query "Philosophy" "What is the concept of sacred time?"
send_query "Philosophy" "How do religions understand death?"
send_query "Philosophy" "What is religious symbolism?"
send_query "Philosophy" "What is the role of doubt in faith?"
send_query "Philosophy" "How do religions view human nature?"
send_query "Philosophy" "What is religious authority?"
send_query "Philosophy" "What is the concept of grace?"

# SECTION 7: Contemporary and Controversial Questions (20 questions)
echo -e "\n${BG_YELLOW}${WHITE}${BOLD} SECTION 7: Contemporary and Controversial Questions ${RESET}"

send_query "Contemporary" "How do religions view LGBTQ+ issues?"
send_query "Contemporary" "What is the role of women in different religions?"
send_query "Contemporary" "How do religions approach environmental issues?"
send_query "Contemporary" "What is religious fundamentalism?"
send_query "Contemporary" "How do religions view artificial intelligence?"
send_query "Contemporary" "What is the relationship between religion and science?"
send_query "Contemporary" "How do religions address mental health?"
send_query "Contemporary" "What is religious extremism?"
send_query "Contemporary" "How do religions view genetic engineering?"
send_query "Contemporary" "What is secularization?"
send_query "Contemporary" "How do religions approach interfaith marriage?"
send_query "Contemporary" "What is the prosperity gospel?"
send_query "Contemporary" "How do religions view abortion?"
send_query "Contemporary" "What is religious nationalism?"
send_query "Contemporary" "How do religions address social justice?"
send_query "Contemporary" "What is the role of religion in politics?"
send_query "Contemporary" "How do religions view euthanasia?"
send_query "Contemporary" "What is religious syncretism?"
send_query "Contemporary" "How do religions approach wealth and poverty?"
send_query "Contemporary" "What is the future of religion?"

# SECTION 8: Challenging and Edge Cases (20 questions)
echo -e "\n${BG_YELLOW}${WHITE}${BOLD} SECTION 8: Challenging and Edge Cases ${RESET}"

send_query "Challenging" "Can an atheist be spiritual?"
send_query "Challenging" "Is Buddhism a religion or philosophy?"
send_query "Challenging" "Why do innocent children suffer if God is good?"
send_query "Challenging" "Can all religions be true simultaneously?"
send_query "Challenging" "Is religious faith incompatible with scientific thinking?"
send_query "Challenging" "Why would a loving God send people to hell?"
send_query "Challenging" "Are religious experiences just psychological phenomena?"
send_query "Challenging" "Can morality exist without religion?"
send_query "Challenging" "Why are there so many religions if there's one truth?"
send_query "Challenging" "Is religion just a coping mechanism?"
send_query "Challenging" "Can God create a stone too heavy for Him to lift?"
send_query "Challenging" "Why do religions have conflicting creation stories?"
send_query "Challenging" "Is religious belief declining globally?"
send_query "Challenging" "Can someone be saved without knowing about God?"
send_query "Challenging" "Why do some prayers go unanswered?"
send_query "Challenging" "Is religion responsible for more harm than good?"
send_query "Challenging" "Can religious texts be interpreted metaphorically?"
send_query "Challenging" "Why do religions change over time?"
send_query "Challenging" "Is there evidence for life after death?"
send_query "Challenging" "Can robots have souls or spiritual experiences?"

# Summary
echo -e "\n${GREEN}${BOLD}✅ All 150 queries completed!${RESET}"
echo -e "${CYAN}Results saved to: ${YELLOW}$OUTPUT_FILE${RESET}"
echo -e "${CYAN}Total questions asked: ${YELLOW}$QUESTION_COUNT${RESET}"

# Generate summary statistics
echo -e "\n${CYAN}${BOLD}Generating summary statistics...${RESET}"
TOTAL_RESPONSES=$(grep -c "^\"[0-9]" "$OUTPUT_FILE")
ERROR_RESPONSES=$(grep -c "\[Error:" "$OUTPUT_FILE")
SUCCESS_RESPONSES=$((TOTAL_RESPONSES - ERROR_RESPONSES))

echo -e "${GREEN}Successful responses: $SUCCESS_RESPONSES${RESET}"
echo -e "${RED}Error responses: $ERROR_RESPONSES${RESET}"

# Print completion message
echo -e "\n${MAGENTA}╔════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${MAGENTA}║${YELLOW}${BOLD}        MasterversAcharya Comprehensive Test Complete        ${MAGENTA}║${RESET}"
echo -e "${MAGENTA}║${WHITE}                    150 Questions Processed                  ${MAGENTA}║${RESET}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════╝${RESET}"

echo -e "\n${CYAN}You can now analyze the responses in ${YELLOW}$OUTPUT_FILE${RESET}"
echo -e "${CYAN}Consider importing into a spreadsheet for detailed analysis.${RESET}"