import requests
import tldextract
import time
import tkinter as tk
from tkinter import ttk

def enumerate_subdomains(domain):
    """Enumerate subdomains of a given domain using a brute-force approach.

    Args:
        domain (str): The target domain name.

    Returns:
        list: A list of discovered subdomains.
    """

    subdomains = []
    wordlist_file = "subdomains.txt"  # Replace with your wordlist file

    try:
        with open(wordlist_file, "r") as f:
            wordlist = f.read().splitlines()

        for word in wordlist:
            subdomain = f"{word}.{domain}"
            url = f"http://{subdomain}"

            try:
                response = requests.get(url, timeout=5)

                if response.status_code == 200:
                    subdomains.append(subdomain)
                    print(f"Found subdomain: {subdomain}")
            except requests.exceptions.RequestException as e:
                # Handle exceptions gracefully (e.g., timeouts, connection errors)
                print(f"Error accessing {url}: {e}")

    except FileNotFoundError:
        print(f"Wordlist file '{wordlist_file}' not found.")

    return subdomains

def start_enumeration():
    domain = domain_entry.get()
    if not domain:
        return

    start_time = time.time()
    discovered_subdomains = enumerate_subdomains(domain)
    end_time = time.time()

    results_tree.delete(*results_tree.get_children())
    for subdomain in discovered_subdomains:
        results_tree.insert("", "end", values=(subdomain,))

    results_label.config(text=f"Enumeration Completed in: {end_time - start_time:.2f} Seconds")
    total_domains_label.config(text=f"Total Domains Captured: {len(discovered_subdomains)}")

# Create the main window
window = tk.Tk()
window.title("Subdomain Enumerator")

# Create labels and entry fields
domain_label = tk.Label(window, text="Enter Target Domain:")
domain_entry = tk.Entry(window, width=50)

# Create a button to start the enumeration
start_button = tk.Button(window, text="Start Enumeration", command=start_enumeration)

# Create labels for results
results_label = tk.Label(window, text="")
total_domains_label = tk.Label(window, text="")

# Create a treeview to display the discovered subdomains
results_tree = ttk.Treeview(window, columns=("Subdomain Name",))
results_tree.heading("#0", text="")
results_tree.heading("Subdomain Name", text="Subdomain Name")
results_tree.column("Subdomain Name", width=200)
results_tree.configure(selectmode="extended")  # Allow multiple item selection

# Bind the selection event to handle dragging
results_tree.bind("<B1-Motion>", lambda event: results_tree.selection_add(event.widget.identify_row(event.y)))

# Arrange the widgets
domain_label.grid(row=0, column=0, padx=5, pady=5)
domain_entry.grid(row=0, column=1, padx=5, pady=5)
start_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
results_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
total_domains_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
results_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Start the GUI loop
window.mainloop()
