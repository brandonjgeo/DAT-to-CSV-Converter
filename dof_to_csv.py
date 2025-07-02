import re
import csv

def dms_to_decimal(deg, min, sec, hemi):
    """Convert DMS to decimal degrees."""
    decimal = int(deg) + int(min) / 60 + float(sec) / 3600
    return -decimal if hemi in ('S', 'W') else decimal

def extract_essentials(line):
    # Extract latitude and longitude in DMS format
    coord_match = re.search(
        r'(\d{2}) (\d{2}) (\d{2}\.\d+)([NS])\s+(\d{3}) (\d{2}) (\d{2}\.\d+)([EW])',
        line
    )
    if not coord_match:
        return None

    lat = dms_to_decimal(*coord_match.groups()[0:4])
    lon = dms_to_decimal(*coord_match.groups()[4:8])

    # Match full obstacle type (1–3 uppercase words after longitude)
    obstacle_type_match = re.search(
        r'\d{3} \d{2} \d{2}\.\d+[EW]\s+([A-Z][A-Z\s\-]{1,40})',
        line
    )
    obstacle_type = obstacle_type_match.group(1).strip() if obstacle_type_match else "UNKNOWN"

    return {
        "Latitude": round(lat, 6),
        "Longitude": round(lon, 6),
        "Obstacle_Type": obstacle_type
    }

def convert_essentials(input_path, output_path):
    with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Latitude", "Longitude", "Obstacle_Type"])
        writer.writeheader()
        for line in infile:
            if re.match(r'^\d{2}-\d{6}', line):  # Line starts with OAS#
                result = extract_essentials(line)
                if result:
                    writer.writerow(result)

if __name__ == "__main__":
    input_path = input("Enter path to DOF.DAT file: ").strip()
    output_path = input("Enter desired output CSV file path: ").strip()
    convert_essentials(input_path, output_path)
    print(f"✅ Extracted coordinates and obstacle types to: {output_path}")
