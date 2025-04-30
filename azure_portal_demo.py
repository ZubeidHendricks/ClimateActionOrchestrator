"""
Climate Action Orchestrator - Azure Portal Demo
This script simulates the Azure Portal interface for the Climate Action Orchestrator
"""

import tkinter as tk
from tkinter import ttk
import time
import threading
import os
import sys
import random

class AzurePortalDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Azure Portal - Climate Action Orchestrator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Set Azure theme colors
        self.azure_blue = "#0078d4"
        self.azure_dark = "#106ebe"
        self.azure_light = "#deecf9"
        self.azure_gray = "#605e5c"
        
        # Create header
        self.header_frame = tk.Frame(root, bg=self.azure_blue, height=50)
        self.header_frame.pack(fill=tk.X)
        
        self.logo_label = tk.Label(self.header_frame, text="Microsoft Azure", fg="white", bg=self.azure_blue, font=("Segoe UI", 14, "bold"))
        self.logo_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Create navigation
        self.nav_frame = tk.Frame(root, bg="#f0f0f0", width=200)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        nav_buttons = [
            "Home", 
            "Resource groups", 
            "AI + Machine Learning", 
            "Azure AI Agent Service", 
            "Storage accounts", 
            "Monitor"
        ]
        
        for btn_text in nav_buttons:
            btn = tk.Button(self.nav_frame, text=btn_text, width=25, 
                           bg="#f0f0f0", fg=self.azure_dark if btn_text == "Azure AI Agent Service" else self.azure_gray,
                           font=("Segoe UI", 9, "bold" if btn_text == "Azure AI Agent Service" else "normal"),
                           borderwidth=0, highlightthickness=0, anchor="w", padx=10)
            btn.pack(fill=tk.X, pady=2)
        
        # Create main content
        self.content_frame = tk.Frame(root, bg="white")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create header for the service
        self.service_header = tk.Frame(self.content_frame, bg="white", height=50)
        self.service_header.pack(fill=tk.X)
        
        self.service_label = tk.Label(self.service_header, text="Climate Action Orchestrator", fg=self.azure_dark, bg="white", font=("Segoe UI", 18, "bold"))
        self.service_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Create tabs
        self.tab_control = ttk.Notebook(self.content_frame)
        
        self.overview_tab = tk.Frame(self.tab_control, bg="white")
        self.agents_tab = tk.Frame(self.tab_control, bg="white")
        self.data_tab = tk.Frame(self.tab_control, bg="white")
        self.analysis_tab = tk.Frame(self.tab_control, bg="white")
        self.recommendations_tab = tk.Frame(self.tab_control, bg="white")
        
        self.tab_control.add(self.overview_tab, text="Overview")
        self.tab_control.add(self.agents_tab, text="AI Agents")
        self.tab_control.add(self.data_tab, text="Data Sources")
        self.tab_control.add(self.analysis_tab, text="Analysis")
        self.tab_control.add(self.recommendations_tab, text="Recommendations")
        
        self.tab_control.pack(expand=1, fill=tk.BOTH)
        
        # Create content for Overview tab
        self.create_overview_tab()
        
        # Create content for AI Agents tab
        self.create_agents_tab()
        
        # Create content for Data Sources tab
        self.create_data_tab()
        
        # Create content for Analysis tab
        self.create_analysis_tab()
        
        # Create content for Recommendations tab
        self.create_recommendations_tab()
        
    def create_overview_tab(self):
        # Overview title
        title_label = tk.Label(self.overview_tab, text="Climate Action Orchestrator - Overview", 
                               font=("Segoe UI", 14, "bold"), bg="white", fg=self.azure_dark)
        title_label.pack(anchor="w", padx=20, pady=10)
        
        # Status frame
        status_frame = tk.Frame(self.overview_tab, bg=self.azure_light, padx=10, pady=10)
        status_frame.pack(fill=tk.X, padx=20, pady=5)
        
        status_label = tk.Label(status_frame, text="Status: Active", 
                                font=("Segoe UI", 12), bg=self.azure_light, fg="green")
        status_label.pack(side=tk.LEFT)
        
        refresh_btn = tk.Button(status_frame, text="Refresh", bg=self.azure_blue, fg="white",
                               font=("Segoe UI", 9), padx=10)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Resource info
        info_frame = tk.Frame(self.overview_tab, bg="white")
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Create a 2x3 grid of info boxes
        for i, (title, value) in enumerate([
            ("Resource Group", "climate-action-rg"),
            ("Location", "East US"),
            ("Subscription", "Azure Subscription 1"),
            ("Resource Type", "Azure AI Agent Service"),
            ("API Endpoint", "climate-action.agent.azure.com"),
            ("Last Updated", "April 30, 2025 09:15 AM")
        ]):
            box_frame = tk.Frame(info_frame, bg="white", relief="ridge", bd=1)
            box_frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            title_label = tk.Label(box_frame, text=title, font=("Segoe UI", 9), bg="white", fg=self.azure_gray)
            title_label.pack(anchor="w", padx=10, pady=5)
            
            value_label = tk.Label(box_frame, text=value, font=("Segoe UI", 11), bg="white")
            value_label.pack(anchor="w", padx=10, pady=5)
        
        # Add column and row configurations to make the grid responsive
        for i in range(3):
            info_frame.columnconfigure(i, weight=1)
        for i in range(2):
            info_frame.rowconfigure(i, weight=1)
        
        # Monitoring graphs
        graph_label = tk.Label(self.overview_tab, text="Monitoring", 
                              font=("Segoe UI", 12, "bold"), bg="white")
        graph_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Placeholder for graphs
        graph_frame = tk.Frame(self.overview_tab, bg="white", height=200)
        graph_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Create 3 sample graph canvases
        for i, title in enumerate(["API Requests", "Agent Activity", "Processing Time"]):
            graph_box = tk.Frame(graph_frame, bg="white", relief="ridge", bd=1)
            graph_box.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
            title_label = tk.Label(graph_box, text=title, font=("Segoe UI", 10), bg="white")
            title_label.pack(anchor="w", padx=10, pady=5)
            
            canvas = tk.Canvas(graph_box, width=300, height=150, bg="white")
            canvas.pack(padx=10, pady=5)
            
            # Draw a sample line graph
            canvas.create_line(50, 120, 100, 80, 150, 100, 200, 50, 250, 70, fill=self.azure_blue, width=2)
            canvas.create_rectangle(50, 120, 250, 140, fill=self.azure_light, outline="")
            
        # Configure the graph frame's grid
        for i in range(3):
            graph_frame.columnconfigure(i, weight=1)
        graph_frame.rowconfigure(0, weight=1)
    
    def create_agents_tab(self):
        # Agents title
        title_label = tk.Label(self.agents_tab, text="AI Agents", 
                               font=("Segoe UI", 14, "bold"), bg="white", fg=self.azure_dark)
        title_label.pack(anchor="w", padx=20, pady=10)
        
        # Create a frame for the agent status and controls
        control_frame = tk.Frame(self.agents_tab, bg=self.azure_light)
        control_frame.pack(fill=tk.X, padx=20, pady=5)
        
        status_label = tk.Label(control_frame, text="All Agents: Active", 
                                font=("Segoe UI", 12), bg=self.azure_light, fg="green")
        status_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        restart_btn = tk.Button(control_frame, text="Restart All Agents", bg=self.azure_blue, fg="white",
                               font=("Segoe UI", 9), padx=10)
        restart_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Create frame for agent list
        agents_list_frame = tk.Frame(self.agents_tab, bg="white")
        agents_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Column headers
        headers_frame = tk.Frame(agents_list_frame, bg=self.azure_blue)
        headers_frame.pack(fill=tk.X)
        
        header_font = ("Segoe UI", 10, "bold")
        header_fg = "white"
        header_bg = self.azure_blue
        header_padx = 10
        header_pady = 5
        
        tk.Label(headers_frame, text="Agent Name", font=header_font, fg=header_fg, bg=header_bg, width=20).pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
        tk.Label(headers_frame, text="Type", font=header_font, fg=header_fg, bg=header_bg, width=15).pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
        tk.Label(headers_frame, text="Status", font=header_font, fg=header_fg, bg=header_bg, width=10).pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
        tk.Label(headers_frame, text="Last Activity", font=header_font, fg=header_fg, bg=header_bg, width=20).pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
        tk.Label(headers_frame, text="Actions", font=header_font, fg=header_fg, bg=header_bg, width=15).pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
        
        # Agent rows
        agents = [
            ("Data Collection Agent", "Collection", "Active", "2 minutes ago"),
            ("Carbon Calculation Agent", "Processing", "Active", "5 minutes ago"),
            ("Recommendation Agent", "Analysis", "Active", "8 minutes ago"),
            ("Simulation Agent", "Modeling", "Active", "15 minutes ago"),
            ("Reporting Agent", "Reporting", "Active", "12 minutes ago")
        ]
        
        for i, (name, type_, status, last_activity) in enumerate(agents):
            row_bg = "#f9f9f9" if i % 2 == 0 else "white"
            row_frame = tk.Frame(agents_list_frame, bg=row_bg)
            row_frame.pack(fill=tk.X)
            
            tk.Label(row_frame, text=name, bg=row_bg, width=20).pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
            tk.Label(row_frame, text=type_, bg=row_bg, width=15).pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
            tk.Label(row_frame, text=status, bg=row_bg, fg="green", width=10).pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
            tk.Label(row_frame, text=last_activity, bg=row_bg, width=20).pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
            
            actions_frame = tk.Frame(row_frame, bg=row_bg)
            actions_frame.pack(side=tk.LEFT, padx=header_padx, pady=header_pady)
            
            tk.Button(actions_frame, text="View", bg=self.azure_blue, fg="white", font=("Segoe UI", 8), padx=5, pady=0).pack(side=tk.LEFT, padx=2)
            tk.Button(actions_frame, text="Restart", bg=self.azure_gray, fg="white", font=("Segoe UI", 8), padx=5, pady=0).pack(side=tk.LEFT, padx=2)
    
    def create_data_tab(self):
        # Data sources title
        title_label = tk.Label(self.data_tab, text="Data Sources", 
                               font=("Segoe UI", 14, "bold"), bg="white", fg=self.azure_dark)
        title_label.pack(anchor="w", padx=20, pady=10)
        
        # Data sources controls
        control_frame = tk.Frame(self.data_tab, bg=self.azure_light)
        control_