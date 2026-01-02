from ocean.clam_lab import deploy_clams
from atmosphere.nano_swarm import deploy_swarms
from relay.satellite_relay import relay_data
from interface.dashboard import launch_dashboard

def main():
    print("🌍 Jarvondis Guardian Network initializing...")
    deploy_clams()
    deploy_swarms()
    relay_data()
    launch_dashboard()

if __name__ == "__main__":
    main()
