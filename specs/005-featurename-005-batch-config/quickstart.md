# Quickstart: Batch Config & Naming

## Validation Scenario 1: Loading & Saving Templates
1. Open the application.
2. Click **New Template**. The tab should say "New Template".
3. Click **Save Template**, name it `my_awesome_template.pdftpl`. 
4. **Verify**: The tab title updates immediately to `my_awesome_template`.
5. Close the tab.
6. Click **Open Template**, select `my_awesome_template.pdftpl`.
7. **Verify**: The new tab is correctly named `my_awesome_template` (not "New Template").

## Validation Scenario 2: Batch Configuration Dialog
1. Open the application.
2. Click **Run Batch Extraction**.
3. Select `my_awesome_template.pdftpl`.
4. Select any folder containing PDFs.
5. Select an output CSV file name.
6. **Verify**: A **Batch Configuration** dialog appears displaying all 3 selected paths.
7. Click **Cancel**.
8. **Verify**: The dialog closes and no batch job runs.
9. Repeat steps 2-6, but click **Start Batch**.
10. **Verify**: The batch extraction executes and generates the output CSV. Open the CSV and verify the template name column says `my_awesome_template`.
