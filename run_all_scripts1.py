import os
import subprocess
import pandas as pd

# ✅ Update these paths
script_folder = r'C:\Users\renny_kurian\PycharmProjects\DTI_ReportBuilder_Services\features\LegacyProductionAutomation\justTestingPurpose'
excel_output_path = r'C:\Users\renny_kurian\PycharmProjects\DTI_ReportBuilder_Services\features\LegacyProductionAutomation\justTestingPurpose\user_data\script_results.xlsx'

results = {
    'Script': [],
    'Status': [],
    'Output': []
}

for filename in os.listdir(script_folder):
    if filename.endswith('.py'):
        script_path = os.path.join(script_folder, filename)
        print(f"Running script: {filename}")  # ✅ Show which script is running
        results['Script'].append(filename)
        try:
            completed = subprocess.run(
                ['python', script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                check=True
            )
            results['Status'].append('Passed')
            results['Output'].append(completed.stdout)
        except subprocess.CalledProcessError as e:
            results['Status'].append('Failed')
            error_output = e.stderr.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
            results['Output'].append(error_output)

df = pd.DataFrame(results)
df.to_excel(excel_output_path, index=False, engine='openpyxl')

print(f"\n✅ Execution results saved to: {excel_output_path}")

"""import os
import subprocess
import pandas as pd

# ✅ Update these paths
script_folder = r'C:\Users\renny_kurian\PycharmProjects\DTI_ReportBuilder_Services\features\LegacyProductionAutomation\justTestingPurpose'
excel_output_path = os.path.join(script_folder, 'user_data', 'script_results.xlsx')

results = {
    'Script': [],
    'Status': [],
    'Output': []
}

for filename in os.listdir(script_folder):
    if filename.endswith('.py'):
        script_path = os.path.join(script_folder, filename)
        print(f"Running script: {filename}")
        results['Script'].append(filename)

        try:
            completed = subprocess.run(
                ['python', script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )

            output = completed.stdout + "\n" + completed.stderr

            # Check for failure message in output
            if "❌ Script failed" in output or completed.returncode != 0:
                results['Status'].append('Failed')
            else:
                results['Status'].append('Passed')

            results['Output'].append(output)

        except Exception as e:
            results['Status'].append('Failed')
            results['Output'].append(str(e))

# Save results to Excel
df = pd.DataFrame(results)
df.to_excel(excel_output_path, index=False, engine='openpyxl')

print(f"\n✅ Execution results saved to: {excel_output_path}")

"""