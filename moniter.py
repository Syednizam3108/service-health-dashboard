import json
from datetime import datetime

# File to store service data
SERVICE_DATA_FILE = "service_data.json"

# Load service data from JSON file
def load_service_data():
    try:
        with open(SERVICE_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"services": []}

# Save service data to JSON file
def save_service_data(data):
    with open(SERVICE_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# CRUD Operations
def create_service(service_id, service_name, status="healthy"):
    data = load_service_data()
    new_service = {
        "service_id": service_id,
        "service_name": service_name,
        "status": status,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "alerts": [],
        "outage_cause": None
    }
    data["services"].append(new_service)
    save_service_data(data)
    print(f"Service '{service_name}' (ID: {service_id}) created successfully.")

def read_services():
    data = load_service_data()
    for service in data["services"]:
        print(json.dumps(service, indent=4))

def update_service_status(service_id, status):
    data = load_service_data()
    for service in data["services"]:
        if service["service_id"] == service_id:
            service["status"] = status
            service["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if status == "unhealthy":
                service["alerts"].append({
                    "message": f"Service {service['service_name']} is unhealthy!",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            save_service_data(data)
            print(f"Service ID {service_id} status updated to '{status}'.")
            return
    print(f"Service ID {service_id} not found.")

def delete_service(service_id):
    data = load_service_data()
    data["services"] = [s for s in data["services"] if s["service_id"] != service_id]
    save_service_data(data)
    print(f"Service ID {service_id} deleted successfully.")

# Outage Analysis
def analyse_outage_cause(service_id):
    data = load_service_data()
    for service in data["services"]:
        if service["service_id"] == service_id:
            if service["status"] == "unhealthy":
                service["outage_cause"] = "Network latency"  # Example cause
                save_service_data(data)
                print(f"Outage cause for Service ID {service_id}: {service['outage_cause']}")
            else:
                print(f"Service ID {service_id} is healthy. No outage detected.")
            return
    print(f"Service ID {service_id} not found.")

# User Interface
def display_menu():
    print("\nService Health Dashboard")
    print("1. Create Service")
    print("2. Read Services")
    print("3. Update Service Status")
    print("4. Delete Service")
    print("5. Analyse Outage Cause")
    print("6. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            service_id = input("Enter Service ID: ")
            service_name = input("Enter Service Name: ")
            create_service(service_id, service_name)

        elif choice == "2":
            read_services()

        elif choice == "3":
            service_id = input("Enter Service ID: ")
            status = input("Enter new status (healthy/unhealthy): ")
            update_service_status(service_id, status)

        elif choice == "4":
            service_id = input("Enter Service ID: ")
            delete_service(service_id)

        elif choice == "5":
            service_id = input("Enter Service ID: ")
            analyse_outage_cause(service_id)

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()