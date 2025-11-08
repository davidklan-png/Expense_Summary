# Demo Files

This folder contains example input and output files demonstrating the Saison Transform pipeline.

## Directory Structure

```
demo/
├── Input/          # Example input transaction CSV
├── Reference/      # Example attendee reference list
└── Output/         # Generated processed CSV and HTML report
```

## Files

### Input/202510_sample.csv
Sample transaction data with 5 rows:
- 3 relevant transactions (会議費/接待費)
- 1 non-relevant transaction (交通費)
- 1 mixed transaction

**Key observations:**
- Input encoding: UTF-8
- Contains required columns: 利用日, ご利用店名及び商品名, 利用金額, 備考
- Transaction amounts range from ¥3,000 to ¥25,000

### Reference/NameList.csv
Sample attendee reference list with 8 attendees:
- ID, Name, Title, Company columns
- Used for populating ID1-ID8 columns in output

### Output/202510_sample.csv
Processed CSV output showing:
- **All 5 rows preserved** (Phase 4)
- Added columns: 出席者, ID1-ID8
- Attendee data populated only for relevant transactions
- Non-relevant row has blank attendee columns

### Output/202510_sample.html
HTML report containing:
- Transaction summary table
- Unique attendee list with details
- Total transaction count and amount

## Running the Demo

### Quick Start (Recommended)

Use the demo runner script:

```bash
# From the demo directory
cd demo
./run-demo.sh
```

This script automatically:
- Creates a temporary directory outside git repository
- Copies demo files to the temporary location
- Runs saisonxform with proper configuration
- Shows output files and offers to open them

### Manual Method

If you prefer to run manually:

```bash
# Copy demo files outside the repository
mkdir -p /tmp/saisonxform-demo/{Input,Reference,Output}
cp demo/Input/* /tmp/saisonxform-demo/Input/
cp demo/Reference/* /tmp/saisonxform-demo/Reference/

# Run the pipeline
poetry run saisonxform run \
  --input /tmp/saisonxform-demo/Input \
  --reference /tmp/saisonxform-demo/Reference \
  --output /tmp/saisonxform-demo/Output \
  --month 202510 \
  --verbose

# View the results
open /tmp/saisonxform-demo/Output/202510_sample.html
```

**Note:** Data directories must be outside git repositories for security. This prevents accidental commits of sensitive financial data.

## Expected Behavior

1. **Encoding Detection**: Auto-detects UTF-8 encoding
2. **Transaction Filtering**: Identifies 4 relevant transactions (会議費/接待費)
3. **Attendee Estimation**: Random count between 2-8 for each transaction
4. **ID Sampling**:
   - Primary ID weighted (90% ID '2', 10% ID '1')
   - Remaining IDs sampled randomly from reference list
   - Sorted numerically, padded to ID8
5. **CSV Output**: All rows preserved, attendee columns added
6. **HTML Report**: Summary with transaction table and unique attendees
7. **Archival**: Input file moved to Archive/202510/ after processing
