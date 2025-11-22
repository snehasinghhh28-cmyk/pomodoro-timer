def get_custom_css():
    return """
    <style>
        /* Main Background */
        .stApp {
            background-color: #1e1e1e;
            color: #d4d4d4;
        }
        
        /* Metrics/Timer text */
        .big-font {
            font-size: 80px !important;
            font-weight: bold;
            color: #64b5f6;
            text-align: center;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* Button Styling */
        .stButton>button {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #444444;
            border-radius: 8px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #444444;
            border-color: #64b5f6;
            color: #64b5f6;
        }
        
        /* Divider */
        hr {
            border-color: #444444;
        }
    </style>
    """