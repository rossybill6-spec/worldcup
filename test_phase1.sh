#!/bin/bash

# Phase 1 Test Script - Tests all Auth endpoints
BASE="http://localhost:8000/api/v1/auth"

echo "========================================="
echo "PHASE 1 - AUTH TEST SUITE"
echo "========================================="
echo ""

# 1. SIGNUP
echo "1. TESTING SIGNUP..."
SIGNUP_RESPONSE=$(curl -s -X POST "$BASE/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-01-15",
    "ssn": "123-45-6789",
    "address_line1": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "username": "johndoe",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!",
    "security_question_1": "What is your pets name?",
    "security_answer_1": "Max",
    "security_question_2": "What city were you born in?",
    "security_answer_2": "Boston",
    "agree_to_terms": true
  }')
echo "$SIGNUP_RESPONSE" | python -m json.tool 2>/dev/null || echo "$SIGNUP_RESPONSE"
echo ""

# 2. GET VERIFICATION CODE
echo "2. GETTING VERIFICATION CODE..."
CODE_RESPONSE=$(curl -s "$BASE/test-verification-code?email=john@example.com")
echo "$CODE_RESPONSE" | python -m json.tool 2>/dev/null || echo "$CODE_RESPONSE"
CODE=$(echo "$CODE_RESPONSE" | python -c "import sys,json; print(json.load(sys.stdin)['code'])" 2>/dev/null)
echo "Code: $CODE"
echo ""

# 3. VERIFY EMAIL
echo "3. VERIFYING EMAIL..."
VERIFY_RESPONSE=$(curl -s -X POST "$BASE/verify-email" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"john@example.com\", \"code\": \"$CODE\"}")
echo "$VERIFY_RESPONSE" | python -m json.tool 2>/dev/null || echo "$VERIFY_RESPONSE"
echo ""

# 4. LOGIN WITH USERNAME
echo "4. TESTING LOGIN (username)..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE/login" \
  -H "Content-Type: application/json" \
  -d '{"login": "johndoe", "password": "TestPass123!"}')
echo "$LOGIN_RESPONSE" | python -m json.tool 2>/dev/null || echo "$LOGIN_RESPONSE"
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python -c "import sys,json; d=json.load(sys.stdin); print(d['data']['access_token'])" 2>/dev/null)
REFRESH_TOKEN=$(echo "$LOGIN_RESPONSE" | python -c "import sys,json; d=json.load(sys.stdin); print(d['data']['refresh_token'])" 2>/dev/null)
echo "Access Token: ${ACCESS_TOKEN:0:50}..."
echo ""

# 5. LOGIN WITH EMAIL
echo "5. TESTING LOGIN (email)..."
curl -s -X POST "$BASE/login" \
  -H "Content-Type: application/json" \
  -d '{"login": "john@example.com", "password": "TestPass123!"}' | python -m json.tool 2>/dev/null
echo ""

# 6. LOGIN WITH WRONG PASSWORD
echo "6. TESTING LOGIN (wrong password)..."
curl -s -X POST "$BASE/login" \
  -H "Content-Type: application/json" \
  -d '{"login": "johndoe", "password": "WrongPass123!"}' | python -m json.tool 2>/dev/null
echo ""

# 7. TOKEN REFRESH
if [ -n "$REFRESH_TOKEN" ]; then
  echo "7. TESTING TOKEN REFRESH..."
  curl -s -X POST "$BASE/refresh-token" \
    -H "Content-Type: application/json" \
    -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}" | python -m json.tool 2>/dev/null
  echo ""
fi

# 8. FORGOT PASSWORD
echo "8. TESTING FORGOT PASSWORD..."
curl -s -X POST "$BASE/forgot-password" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}' | python -m json.tool 2>/dev/null
echo ""

# 9. FORGOT USERNAME
echo "9. TESTING FORGOT USERNAME..."
curl -s -X POST "$BASE/forgot-username" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}' | python -m json.tool 2>/dev/null
echo ""

# 10. DUPLICATE SIGNUP
echo "10. TESTING DUPLICATE SIGNUP..."
curl -s -X POST "$BASE/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-01-15",
    "ssn": "123-45-6789",
    "address_line1": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "username": "johndoe",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!",
    "security_question_1": "What is your pets name?",
    "security_answer_1": "Max",
    "security_question_2": "What city were you born in?",
    "security_answer_2": "Boston",
    "agree_to_terms": true
  }' | python -m json.tool 2>/dev/null
echo ""

# 11. PROTECTED ROUTE TEST
if [ -n "$ACCESS_TOKEN" ]; then
  echo "11. TESTING PROTECTED ROUTE (with token)..."
  curl -s "http://localhost:8000/api/v1/health" \
    -H "Authorization: Bearer $ACCESS_TOKEN" | python -m json.tool 2>/dev/null
  echo ""
fi

# 12. LOGOUT
if [ -n "$ACCESS_TOKEN" ]; then
  echo "12. TESTING LOGOUT..."
  curl -s -X POST "$BASE/logout" \
    -H "Authorization: Bearer $ACCESS_TOKEN" | python -m json.tool 2>/dev/null
  echo ""
fi

echo "========================================="
echo "PHASE 1 TESTS COMPLETE"
echo "========================================="
