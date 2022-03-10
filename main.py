from tkinter import *
from tkinter import ttk
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import black_scholes as bs
from api_functions import get_positions, get_instrument, get_order_book, get_instruments

# CHANGE THE GREEKS CALCULATIONS TO INCLUDE POSITION SIZES
# CHANGE THE GREEKS CALCULATIONS TO INCLUDE POSITION SIZES
# CHANGE THE GREEKS CALCULATIONS TO INCLUDE POSITION SIZES

step_number = 100
chart_size = (4, 2.75)

root = Tk()
root.title("Deribit API in Python - Cryptarbitrage")
root.iconbitmap('cryptarbitrage_icon_96px.ico')
root.minsize(600, 200)

style = ttk.Style()
style.theme_use("alt")
style.configure("Treeview", fieldbackground="#102831")
style.configure("Treeview.Heading", background="#0c1b21", foreground="#aaaaaa", borderwidth=0)
# Details input frame
details_frame = LabelFrame(root, text="Details", padx=2, pady=2)
details_frame.grid(row=0, column=0, padx=2, pady=2, sticky=NW)
# Chart frames
delta_frame = LabelFrame(root, text="Delta", padx=2, pady=2)
delta_frame.grid(row=0, column=1, padx=2, pady=2)
gamma_frame = LabelFrame(root, text="Gamma", padx=2, pady=2)
gamma_frame.grid(row=0, column=2, padx=2, pady=2)
vega_frame = LabelFrame(root, text="Vega", padx=2, pady=2)
vega_frame.grid(row=1, column=1, padx=2, pady=2)
theta_frame = LabelFrame(root, text="Theta", padx=2, pady=2)
theta_frame.grid(row=1, column=2, padx=2, pady=2)

positions_frame = LabelFrame(root, text="Positions", padx=10, pady=10)
positions_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
#positions_frame.grid_rowconfigure(0, weight=1)
#positions_frame.grid_columnconfigure(0, weight=1)

# Treeview scrollbar
pos_tree_scroll = Scrollbar(positions_frame)
# Treeview
pos_tree = ttk.Treeview(positions_frame, selectmode='none', yscrollcommand=pos_tree_scroll.set)
pos_tree_scroll.config(command=pos_tree.yview, background="#000000")
pos_tree['columns'] = ("Type", "Instrument", "Size", "Value", "Delta", "Gamma", "Vega", "Theta")
pos_tree.column("#0", width=80)
pos_tree.column("Type", anchor=W, width=60)
pos_tree.column("Instrument", width=140)
pos_tree.column("Size", anchor=E, width=120)
pos_tree.column("Value", anchor=E, width=140)
pos_tree.column("Delta", anchor=E, width=100)
pos_tree.column("Gamma", anchor=E, width=100)
pos_tree.column("Vega", anchor=E, width=100)
pos_tree.column("Theta", anchor=E, width=100)

pos_tree.heading("#0", text="Currency")
pos_tree.heading("Type", text="Type", anchor=W)
pos_tree.heading("Instrument", text="Instrument", anchor=W)
pos_tree.heading("Size", text="Size", anchor=E)
pos_tree.heading("Value", text="Value", anchor=E)
pos_tree.heading("Delta", text="Delta", anchor=E)
pos_tree.heading("Gamma", text="Gamma", anchor=E)
pos_tree.heading("Vega", text="Vega", anchor=E)
pos_tree.heading("Theta", text="Theta", anchor=E)

pos_tree.tag_configure('total', background="#193e4c", foreground="#ffffff")
pos_tree.tag_configure('odd', background="#0c1b21", foreground="#ffffff")
pos_tree.tag_configure('even', background="#102831", foreground="#ffffff")

pos_tree.grid(row=0, column=0, sticky=NS)
pos_tree_scroll.grid(row=0, column=1, sticky=NS)


def calculate_greeks(position_list, nearest_date):
    current_date = int(time.time()) * 1000
    max_calc_date = nearest_date - current_date
    time_points = [current_date + max_calc_date * (1-1),
                   current_date + max_calc_date * (1-0.7),
                   current_date + max_calc_date * (1-0.3),
                   current_date + max_calc_date * (1-0.1)]
    # DELTA
    all_deltas = []
    for time_point in time_points:
        position_deltas = []
        for position in position_list:
            if position['kind'] == 'future':
                temp_pos_delta = []
                chart_low = float(chart_minprice_input.get())
                chart_high = float(chart_maxprice_input.get())
                for step in range(0, step_number + 1):
                    temp_pos_delta.append(position['size']/(step * (chart_high - chart_low) / step_number + chart_low))
                position_deltas.append(temp_pos_delta)
            elif position['kind'] == 'option':
                temp_pos_delta = []
                chart_low = float(chart_minprice_input.get())
                chart_high = float(chart_maxprice_input.get())
                for step in range(0, step_number + 1):
                    S = step * (chart_high - chart_low) / step_number + chart_low
                    K = float(position['strike'])
                    T = (float(position['expiration_timestamp']-time_point)/1000)/(60*60*24)/365
                    R= 0
                    sigma = float(position['mark_iv'])/100
                    if position['option_type'] == "call":
                        op_type = "C"
                    else:
                        op_type = "P"
                    temp_pos_delta.append(bs.bs_delta(S, K, T, R, sigma, op_type) * position['size'])
                position_deltas.append(temp_pos_delta)
        delta_total = [0] * (step_number + 1)
        for position in position_deltas:
            for step in range(0, step_number + 1):
                delta_total[step] = delta_total[step] + position[step]
        all_deltas.append(delta_total)

    # GAMMA
    all_gammas = []
    for time_point in time_points:
        position_gammas = []
        for position in position_list:
            if position['kind'] == 'future':
                temp_pos_gamma = []
                for step in range(0, step_number + 1):
                    temp_pos_gamma.append(0)
                position_gammas.append(temp_pos_gamma)
            elif position['kind'] == 'option':
                temp_pos_gamma = []
                chart_low = float(chart_minprice_input.get())
                chart_high = float(chart_maxprice_input.get())
                for step in range(0, step_number + 1):
                    S = step * (chart_high - chart_low) / step_number + chart_low
                    K = float(position['strike'])
                    T = (float(position['expiration_timestamp'] - time_point) / 1000) / (60 * 60 * 24) / 365
                    R = 0
                    sigma = float(position['mark_iv']) / 100
                    temp_pos_gamma.append(bs.bs_gamma(S, K, T, R, sigma) * position['size'])
                position_gammas.append(temp_pos_gamma)
        gamma_total = [0] * (step_number + 1)
        for position in position_gammas:
            for step in range(0, step_number + 1):
                gamma_total[step] = gamma_total[step] + position[step]
        all_gammas.append(gamma_total)

    # VEGA
    all_vegas = []
    for time_point in time_points:
        position_vegas = []
        for position in position_list:
            if position['kind'] == 'future':
                temp_pos_vega = []
                for step in range(0, step_number + 1):
                    temp_pos_vega.append(0)
                position_vegas.append(temp_pos_vega)
            elif position['kind'] == 'option':
                temp_pos_vega = []
                chart_low = float(chart_minprice_input.get())
                chart_high = float(chart_maxprice_input.get())
                for step in range(0, step_number + 1):
                    S = step * (chart_high - chart_low) / step_number + chart_low
                    K = float(position['strike'])
                    T = (float(position['expiration_timestamp'] - time_point) / 1000) / (60 * 60 * 24) / 365
                    R = 0
                    sigma = float(position['mark_iv']) / 100
                    temp_pos_vega.append(bs.bs_vega(S, K, T, R, sigma) * position['size'])
                position_vegas.append(temp_pos_vega)
        vega_total = [0] * (step_number + 1)
        for position in position_vegas:
            for step in range(0, step_number + 1):
                vega_total[step] = vega_total[step] + position[step]
        all_vegas.append(vega_total)

    # THETA
    all_thetas = []
    for time_point in time_points:
        position_thetas = []
        for position in position_list:
            if position['kind'] == 'future':
                temp_pos_theta = []
                for step in range(0, step_number + 1):
                    temp_pos_theta.append(0)
                position_thetas.append(temp_pos_theta)
            elif position['kind'] == 'option':
                temp_pos_theta = []
                chart_low = float(chart_minprice_input.get())
                chart_high = float(chart_maxprice_input.get())
                for step in range(0, step_number + 1):
                    S = step * (chart_high - chart_low) / step_number + chart_low
                    K = float(position['strike'])
                    T = (float(position['expiration_timestamp'] - time_point) / 1000) / (60 * 60 * 24) / 365
                    R = 0
                    sigma = float(position['mark_iv']) / 100
                    if position['option_type'] == "call":
                        op_type = "C"
                    else:
                        op_type = "P"
                    temp_pos_theta.append(bs.bs_theta(S, K, T, R, sigma, op_type) * position['size'])
                position_thetas.append(temp_pos_theta)
        theta_total = [0] * (step_number + 1)
        for position in position_thetas:
            for step in range(0, step_number + 1):
                theta_total[step] = theta_total[step] + position[step]
        all_thetas.append(theta_total)

    return all_deltas, all_gammas, all_vegas, all_thetas, max_calc_date


def plot_charts(all_deltas, all_gammas, all_vegas, all_thetas, max_calc_date):
    # Destroy old charts if any
    for widgets in delta_frame.winfo_children():
        widgets.destroy()
    for widgets in gamma_frame.winfo_children():
        widgets.destroy()
    for widgets in vega_frame.winfo_children():
        widgets.destroy()
    for widgets in theta_frame.winfo_children():
        widgets.destroy()
    # Generate x axis values
    x_range = []
    chart_low = float(chart_minprice_input.get())
    chart_high = float(chart_maxprice_input.get())
    for step in range(0, step_number + 1):
        x_range.append(step * (chart_high - chart_low) / 100 + chart_low)
    # Some chart styling
    line_colours = ['#2fd524', '#173277', '#2859d1', '#6185e0']
    line_widths = [2, 1.5, 1.5, 1.5]
    line_alphas = [1, 0.8, 0.8, 0.8]
    max_days = float(max_calc_date/1000)/(60*60*24)
    time_labels = ['Today', '+' + str(round(max_days * 0.3, 2)) + 'd', '+' + str(round(max_days * 0.6, 2)) + 'd', '+' + str(round(max_days * 0.9, 2)) + 'd']
    # DELTA CHART
    fig_delta = Figure(figsize=chart_size, dpi=100)
    plot_delta = fig_delta.add_subplot(111)
    # plotting the graph
    chart_item_count = 0
    for item in all_deltas:
        plot_delta.plot(x_range, all_deltas[chart_item_count], color=line_colours[chart_item_count], linewidth=line_widths[chart_item_count], label=time_labels[chart_item_count], alpha=line_alphas[chart_item_count])
        chart_item_count = chart_item_count + 1
    plot_delta.set_xlabel('Underlying Price')
    plot_delta.set_ylabel('Delta')
    plot_delta.legend()
    plot_delta.grid(True)
    fig_delta.tight_layout()
    # creating the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig_delta, master=delta_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, delta_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

    # GAMMA CHART
    fig_gamma = Figure(figsize=chart_size, dpi=100)
    plot_gamma = fig_gamma.add_subplot(111)
    # plotting the graph
    chart_item_count = 0
    for item in all_gammas:
        plot_gamma.plot(x_range, all_gammas[chart_item_count], color=line_colours[chart_item_count],
                        linewidth=line_widths[chart_item_count], label=time_labels[chart_item_count], alpha=line_alphas[chart_item_count])
        chart_item_count = chart_item_count + 1
    plot_gamma.set_xlabel('Underlying Price')
    plot_gamma.set_ylabel('Gamma')
    plot_gamma.legend()
    plot_gamma.grid(True)
    fig_gamma.tight_layout()
    # creating the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig_gamma, master=gamma_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, gamma_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

    # VEGA CHART
    fig_vega = Figure(figsize=chart_size, dpi=100)
    plot_vega = fig_vega.add_subplot(111)
    # plotting the graph
    chart_item_count = 0
    for item in all_vegas:
        plot_vega.plot(x_range, all_vegas[chart_item_count], color=line_colours[chart_item_count],
                        linewidth=line_widths[chart_item_count], label=time_labels[chart_item_count], alpha=line_alphas[chart_item_count])
        chart_item_count = chart_item_count + 1
    plot_vega.set_xlabel('Underlying Price')
    plot_vega.set_ylabel('Vega')
    plot_vega.legend()
    plot_vega.grid(True)
    fig_vega.tight_layout()
    # creating the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig_vega, master=vega_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, vega_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

    # THETA CHART
    fig_theta = Figure(figsize=chart_size, dpi=100)
    plot_theta = fig_theta.add_subplot(111)
    # plotting the graph
    chart_item_count = 0
    for item in all_thetas:
        plot_theta.plot(x_range, all_thetas[chart_item_count], color=line_colours[chart_item_count],
                        linewidth=line_widths[chart_item_count], label=time_labels[chart_item_count], alpha=line_alphas[chart_item_count])
        chart_item_count = chart_item_count + 1
    plot_theta.set_xlabel('Underlying Price')
    plot_theta.set_ylabel('Theta')
    plot_theta.legend()
    plot_theta.grid(True)
    fig_theta.tight_layout()
    # creating the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig_theta, master=theta_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, theta_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

    plt.show()

def calculate_greeks_click():
    # Select the correct currency positions
    position_list = []
    if selected_currency.get() == "BTC":
        position_list = positions_list_btc
    elif selected_currency.get() == "ETH":
        position_list = positions_list_eth
    elif selected_currency.get() == "SOL":
        position_list = positions_list_sol
    # Create list of instrument names
    instrument_list = []
    for position in position_list:
        instrument_list.append(position['instrument_name'])
    print("instrument list", instrument_list)
    # Call get instruments for all instruments of chosen currency
    all_instruments = get_instruments(selected_currency.get())
    # Pull in order book details from api and add to position list
    instrument_details = []
    for instrument in instrument_list:
        current_instrument = instrument
        for entry in all_instruments:
            if entry.get("instrument_name") == current_instrument:
                instrument_details.append(entry)
    for position in position_list:
        current_instrument = position['instrument_name']
        for instrument in instrument_details:
            if instrument.get("instrument_name") == current_instrument:
                position.update(instrument)
    # Pull in order book details from api and add to position list
    book_details = []
    for instrument in instrument_list:
        book_details.append(get_order_book(instrument))
    for position in position_list:
        current_instrument = position['instrument_name']
        for instrument in book_details:
            if instrument.get("instrument_name") == current_instrument:
                position.update(instrument)

    print("position list", position_list)
    # Determine nearest expiry date
    nearest_date_list = []
    for instrument in instrument_details:
        nearest_date_list.append(instrument.get("expiration_timestamp"))
    nearest_date = sorted(nearest_date_list)[0]
    print("nearest date", nearest_date)

    all_deltas, all_gammas, all_vegas, all_thetas, max_calc_date = calculate_greeks(position_list, nearest_date)

    plot_charts(all_deltas, all_gammas, all_vegas, all_thetas, max_calc_date)


def get_positions_click():
    for widgets in positions_frame.winfo_children():
        widgets.destroy()
    global positions_list_btc, positions_list_eth, positions_list_sol
    positions_list_btc, positions_list_eth, positions_list_sol = get_positions()
    # Size totals
    btc_size = 0.0
    eth_size = 0.0
    sol_size = 0.0
    for position in positions_list_btc:
        btc_size = btc_size + position['size']
    for position in positions_list_eth:
        eth_size = eth_size + position['size']
    for position in positions_list_sol:
        sol_size = sol_size + position['size']
    # Delta totals
    btc_delta = 0.0
    eth_delta = 0.0
    sol_delta = 0.0
    for position in positions_list_btc:
        btc_delta = btc_delta + position['delta']
        position['delta'] = round(position['delta'], 4)
    for position in positions_list_eth:
        eth_delta = eth_delta + position['delta']
        position['delta'] = round(position['delta'], 4)
    for position in positions_list_sol:
        sol_delta = sol_delta + position['delta']
        position['delta'] = round(position['delta'], 4)
    btc_delta = round(btc_delta, 4)
    eth_delta = round(eth_delta, 4)
    sol_delta = round(sol_delta, 4)
    # Gamma totals
    btc_gamma = 0.0
    eth_gamma = 0.0
    sol_gamma = 0.0
    for position in positions_list_btc:
        btc_gamma = btc_gamma + position.get('gamma', 0)
        position['gamma'] = round(position.get('gamma', 0), 4)
    for position in positions_list_eth:
        eth_gamma = eth_gamma + position.get('gamma', 0)
        position['gamma'] = round(position.get('gamma', 0), 4)
    for position in positions_list_sol:
        sol_gamma = sol_gamma + position.get('gamma', 0)
        position['gamma'] = round(position.get('gamma', 0), 4)
    btc_gamma = round(btc_gamma, 4)
    eth_gamma = round(eth_gamma, 4)
    sol_gamma = round(sol_gamma, 4)
    # Vega totals
    btc_vega = 0.0
    eth_vega = 0.0
    sol_vega = 0.0
    for position in positions_list_btc:
        btc_vega = btc_vega + position.get('vega', 0)
        position['vega'] = round(position.get('vega', 0), 4)
    for position in positions_list_eth:
        eth_vega = eth_vega + position.get('vega', 0)
        position['vega'] = round(position.get('vega', 0), 4)
    for position in positions_list_sol:
        sol_vega = sol_vega + position.get('vega', 0)
        position['vega'] = round(position.get('vega', 0), 4)
    btc_vega = round(btc_vega, 4)
    eth_vega = round(eth_vega, 4)
    sol_vega = round(sol_vega, 4)
    # Theta totals
    btc_theta = 0.0
    eth_theta = 0.0
    sol_theta = 0.0
    for position in positions_list_btc:
        btc_theta = btc_theta + position.get('theta', 0)
        position['theta'] = round(position.get('theta', 0), 4)
    for position in positions_list_eth:
        eth_theta = eth_theta + position.get('theta', 0)
        position['theta'] = round(position.get('theta', 0), 4)
    for position in positions_list_sol:
        sol_theta = sol_theta + position.get('theta', 0)
        position['theta'] = round(position.get('theta', 0), 4)
    btc_theta = round(btc_theta, 4)
    eth_theta = round(eth_theta, 4)
    sol_theta = round(sol_theta, 4)
    # Treeview scrollbar
    pos_tree_scroll = Scrollbar(positions_frame)
    # Treeview
    pos_tree = ttk.Treeview(positions_frame, selectmode='none', yscrollcommand=pos_tree_scroll.set)
    pos_tree_scroll.config(command=pos_tree.yview, background="#000000")
    pos_tree['columns'] = ("Type", "Instrument", "Size", "Value", "Delta", "Gamma", "Vega", "Theta")
    pos_tree.column("#0", width=80)
    pos_tree.column("Type", anchor=W, width=60)
    pos_tree.column("Instrument", width=140)
    pos_tree.column("Size", anchor=E, width=120)
    pos_tree.column("Value", anchor=E, width=140)
    pos_tree.column("Delta", anchor=E, width=100)
    pos_tree.column("Gamma", anchor=E, width=100)
    pos_tree.column("Vega", anchor=E, width=100)
    pos_tree.column("Theta", anchor=E, width=100)

    pos_tree.heading("#0", text="Currency")
    pos_tree.heading("Type", text="Type", anchor=W)
    pos_tree.heading("Instrument", text="Instrument", anchor=W)
    pos_tree.heading("Size", text="Size", anchor=E)
    pos_tree.heading("Value", text="Value", anchor=E)
    pos_tree.heading("Delta", text="Delta", anchor=E)
    pos_tree.heading("Gamma", text="Gamma", anchor=E)
    pos_tree.heading("Vega", text="Vega", anchor=E)
    pos_tree.heading("Theta", text="Theta", anchor=E)

    pos_tree.tag_configure('total', background="#193e4c", foreground="#ffffff")
    pos_tree.tag_configure('odd', background="#0c1b21", foreground="#ffffff")
    pos_tree.tag_configure('even', background="#102831", foreground="#ffffff")

    count = 0
    if positions_list_btc:
        pos_tree.insert(parent='', index='end', iid=count, text="BTC", open=TRUE, values=("", "", btc_size, "", btc_delta, btc_gamma, btc_vega, btc_theta), tags=('total',))
        btc_parent = count
        count += 1

    for position in positions_list_btc:
        if count % 2 == 0:
            pos_tree.insert(parent=btc_parent, index='end', iid=count, text="", values=(position.get('kind'), position.get('instrument_name'), position.get('size'), position.get('size_currency'), position.get('delta'), position.get('gamma'), position.get('vega'), position.get('theta')), tags=('even',))
        else:
            pos_tree.insert(parent=btc_parent, index='end', iid=count, text="", values=(position.get('kind'), position.get('instrument_name'), position.get('size'), position.get('size_currency'), position.get('delta'), position.get('gamma'), position.get('vega'), position.get('theta')), tags=('odd',))
        count += 1

    if positions_list_eth:
        pos_tree.insert(parent='', index='end', iid=count, text="ETH", open=TRUE, values=("", "", eth_size, "", eth_delta, eth_gamma, eth_vega, eth_theta), tags=('total',))
        eth_parent = count
        count += 1

    for position in positions_list_eth:
        if count % 2 == 0:
            pos_tree.insert(parent=eth_parent, index='end', iid=count, text="", values=(position.get('kind'), position.get('instrument_name'), position.get('size'), position.get('size_currency'), position.get('delta'), position.get('gamma'), position.get('vega'), position.get('theta')), tags=('even',))
        else:
            pos_tree.insert(parent=eth_parent, index='end', iid=count, text="", values=(position.get('kind'), position.get('instrument_name'), position.get('size'), position.get('size_currency'), position.get('delta'), position.get('gamma'), position.get('vega'), position.get('theta')), tags=('odd',))
        count += 1

    if positions_list_sol:
        pos_tree.insert(parent='', index='end', iid=count, text="SOL", open=TRUE, values=("", "", sol_size, "", sol_delta, sol_gamma, sol_vega, sol_theta), tags=('total',))
        sol_parent = count
        count += 1

    for position in positions_list_sol:
        if count % 2 == 0:
            pos_tree.insert(parent=sol_parent, index='end', iid=count, text="", values=(position.get('kind'), position.get('instrument_name'), position.get('size'), position.get('size_currency'), position.get('delta'), position.get('gamma'), position.get('vega'), position.get('theta')), tags=('even',))
        else:
            pos_tree.insert(parent=sol_parent, index='end', iid=count, text="", values=(position.get('kind'), position.get('instrument_name'), position.get('size'), position.get('size_currency'), position.get('delta'), position.get('gamma'), position.get('vega'), position.get('theta')), tags=('odd',))
        count += 1

    pos_tree.grid(row=0, column=0, sticky=NS)
    pos_tree_scroll.grid(row=0, column=1, sticky=NS)

    calculate_greeks_button = Button(details_frame, text="Calculate Greeks", command=calculate_greeks_click, padx=12, pady=2, bg="#88bb88")
    calculate_greeks_button.grid(row=3, column=1, padx=5, pady=5)


# Details frame components
selected_currency = StringVar()
selected_currency.set("BTC")
currency_dropdown_label = Label(details_frame, text="Currency: ")
currency_dropdown_label.grid(row=0, column=0)
currency_dropdown = OptionMenu(details_frame, selected_currency, "BTC", "ETH", "SOL")
currency_dropdown.grid(row=0, column=1)
currency_dropdown.config(width=10)

chart_minprice_label = Label(details_frame, text="Chart Min Price: ")
chart_minprice_label.grid(row=1, column=0)
chart_minprice_input = Entry(details_frame, width=15)
chart_minprice_input.grid(row=1, column=1, padx=5, pady=5)

chart_maxprice_label = Label(details_frame, text="Chart Max Price: ")
chart_maxprice_label.grid(row=2, column=0)
chart_maxprice_input = Entry(details_frame, width=15)
chart_maxprice_input.grid(row=2, column=1, padx=5, pady=5)

get_positions_button = Button(details_frame, text="Refresh Positions", command=get_positions_click, padx=2, pady=2)
get_positions_button.grid(row=3, column=0, sticky="w")

pos_col_heads = [
    "Type",
    "Instrument",
    "Size",
    "Value",
    "Delta",
    "Gamma",
    "Vega",
    "Theta",
]

root.mainloop()

