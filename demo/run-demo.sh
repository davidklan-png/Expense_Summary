#!/bin/bash
# Demo runner script for saisonxform
# This script runs saisonxform in demo mode by creating a temporary directory outside git

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Saisonxform Demo Runner ===${NC}\n"

# Get absolute path to demo directory
DEMO_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$DEMO_DIR")"

# Create temporary directory outside git repo
TEMP_DIR="/tmp/saisonxform-demo-$$"
echo -e "${YELLOW}Creating temporary demo directory: ${TEMP_DIR}${NC}"

mkdir -p "$TEMP_DIR"/{Input,Reference,Output,Archive}

# Copy demo files to temporary directory
echo -e "${YELLOW}Copying demo files...${NC}"
cp -r "$DEMO_DIR"/Input/* "$TEMP_DIR/Input/" 2>/dev/null || true
cp -r "$DEMO_DIR"/Reference/* "$TEMP_DIR/Reference/" 2>/dev/null || true

# Run saisonxform
echo -e "\n${GREEN}Running saisonxform...${NC}\n"
cd "$PROJECT_ROOT"
poetry run saisonxform run \
  --input "$TEMP_DIR/Input" \
  --reference "$TEMP_DIR/Reference" \
  --output "$TEMP_DIR/Output" \
  --archive "$TEMP_DIR/Archive" \
  --verbose

# Show results
echo -e "\n${GREEN}=== Demo Complete ===${NC}\n"
echo -e "${BLUE}Output files:${NC}"
ls -lh "$TEMP_DIR/Output/"

echo -e "\n${BLUE}HTML reports:${NC}"
ls -lh "$TEMP_DIR/Output/"*.html 2>/dev/null || echo "No HTML reports generated"

echo -e "\n${YELLOW}Temporary directory: ${TEMP_DIR}${NC}"
echo -e "${YELLOW}Files will remain until you delete them or reboot${NC}\n"

# Optionally open output directory
if [[ "$OSTYPE" == "darwin"* ]]; then
  read -p "Open output directory in Finder? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "$TEMP_DIR/Output"
  fi
fi
