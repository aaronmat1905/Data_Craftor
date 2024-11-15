from CraftorSkeleton import Craftor
import gradio as gr

craftor = Craftor()

def build_interface():
    with gr.Blocks(theme='JohnSmith9982/small_and_pretty') as demo:
        session_id = gr.State(generate_session_id)
        
        gr.HTML("""
        <div>
            <style>
                .header {
                    display: flex;
                    align-items: center;
                    padding: 20px;
                    background-color: #f5f5f5;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                    font-family: Arial, sans-serif;
                }
                .header img {
                    width: 100px;
                    height: 100px;
                    margin-right: 20px;
                    border-radius: 50%;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                }
                .header-text {
                    color: #333;
                    font-size: 48px;
                    font-weight: bold;
                    line-height: 1;
                }
                .header-subtext {
                    color: #666;
                    font-size: 20px;
                    font-weight: 500;
                    margin-top: 5px;
                }
            </style>
            
            <div class="header">
                <img src="DataCraftor/DataCraftorLogo1.png" alt="DataCraftor Logo">
                <div>
                    <div class="header-text">DataCraftor</div>
                    <div class="header-subtext">Synthetic Dataset Generator Platform</div>
                </div>
            </div>
        </div>
        """)
        with gr.Tabs():
            # Introduction tab
            with gr.Tab("Overview"):
                gr.Markdown("""
                    # DataCraftor
                    **DataCraftor** is a comprehensive platform for generating and interacting with synthetic and custom datasets. It offers dynamic updates, data augmentation, statistical processing, and exploratory data analysis (EDA), all accessible through a single chat interface. Users simply input their dataset requirements, and DataCraftor quickly generates tailored synthetic data suited for various industries and applications, with options to seed from existing datasets if desired. This platform enables efficient, privacy-safe data generation, allowing for over 100 data points in seconds.
                    - The interactive chat feature also allows users to upload and engage with their own datasets. Through this feature, users can explore, edit, and refine their data without complex coding—whether that involves cleaning, filtering, or applying transformations. This makes it easy to query specific data insights, make real-time adjustments, and generate new data variations, all in a responsive, user-friendly environment. DataCraftor empowers users to customize and optimize their datasets interactively, providing hands-on control over data processing and enhancement.

                """)

            # Platform Overview tab
            with gr.Tab("What is Synthetic Data?"):
                gr.Markdown("""
                    ## What is Synthetic Data?
                    Synthetic data is artificially generated to replicate the statistical characteristics of real-world data. It is especially valuable in situations where accessing or sharing real data is constrained due to privacy regulations or security concerns. Synthetic data offers a versatile, privacy-safe solution for industries such as healthcare and finance, allowing data-driven innovation without exposing sensitive information.

                    ### Applications and Benefits
                    - **Data Privacy and Security**: Synthetic data preserves statistical structures without including sensitive information, helping ensure compliance with data privacy laws like GDPR and CCPA.
                    - **Cost-Effective and Rapid Generation**: Generating synthetic data is often faster and more affordable than gathering real-world data.
                    - **Enhanced Scenario Testing**: Allows testing of rare or specialized conditions, improving model robustness.
                    - **Education and Training**: Enables hands-on learning in data science without risking real-world data privacy.
                """)

            # Key Functionalities tab
            with gr.Tab("Key Functionalities"):
                gr.Markdown("""
                    ## Key Functionalities
                    - **Synthetic Dataset Generation**: Create datasets based on specific requirements to suit various applications.
                    - **Data Exploration**: Interact and query datasets in real-time to gain insights.
                    - **Dynamic Data Processing**: Upload personal datasets to refine, clean, or augment as needed.
                """)
                
                gr.Markdown("### Data Export Options")
                gr.Markdown("""
                    DataCraftor supports various export formats for flexibility across workflows:
                    - **Code Formats**: Python, SQL, R
                    - **File Formats**: CSV, JSON
                """)
        gr.Markdown("---") 
        with gr.Row():
            with gr.Column():
                chatbot = gr.Chatbot()
                message = gr.Textbox(placeholder="Type your dataset requirements here...")
                clearButton = gr.Button("Clear")
                seeButton = gr.Button("See Generated data")
                
                gr.Examples(
                    examples=[
                        "Generate synthetic dataset for a retail sales department in India with 50 datapoints. Column names are: ID, Product Name, Sales Region, Quantity Sold, Price per Unit [INR], Total Sales [Price per Unit * Quantity Sold], Salesperson ID, Discount Percentage [Apply a 10% discount for orders over 100 units, and 5% for smaller quantities].",
                        "Generate synthetic dataset for an online education platform in India with 30 datapoints. Column names are: Student ID, Course Name, Duration (months), Course Fee [INR], Enrollment Date, Completion Status [Completed/Incomplete], Scholarship Amount [Apply 20% discount for students with a GPA over 8].",
                        "Generate synthetic dataset for a hospital in India with 40 datapoints. Column names are: Patient ID, Age, Gender, Medical Condition, Treatment Cost [INR], Insurance Coverage [Percentage], Final Billing Amount [Apply a 30% discount on treatments for senior citizens (above 60 years)].",
                        "Generate synthetic dataset for stock market data in India with 50 datapoints. Column names are: Stock Symbol, Date, Open Price [INR], Close Price [INR], High Price [INR], Low Price [INR], Trading Volume, Market Capitalization [INR], Price Change Percentage [Calculate based on Open and Close Price].",
                        "Generate synthetic dataset for a smart manufacturing plant in India with 50 datapoints. Column names are: Machine ID, Production Date, Product Type, Units Produced, Production Efficiency [Percentage], Defective Units [Percentage], Maintenance Status [Operational/Under Maintenance], Energy Consumption [kWh], Carbon Emission [kgCO2], Downtime Duration [hours], Maintenance Cost [INR]. [Apply a 15% efficiency increase for machines serviced within the last 3 months]."
                    ],
                    inputs=message
                )

            with gr.Column():
                output_df = gr.Dataframe(interactive=True)

                with gr.Tab("Export Generated Data"):
                    format_dropdown = gr.Dropdown(["python", "SQL", "csv", "R", "json"], label="Convert Data To")
                    outputBOX = gr.Textbox(placeholder="Your output data will be generated as code here.")
                    codeConvert = gr.Button("Get Code")
                    codeConvert.click(fn= craftor.convert_data, inputs=[format_dropdown, session_id], outputs=outputBOX)
                
                with gr.Tab("Use Your Data"):
                    file_input = gr.File(label="Upload CSV File", file_types=[".csv"])
                    chatFileInput = gr.Button("Chat with This Data")
                    file_input.change(fn=craftor.upload_file, inputs=file_input, outputs=output_df)
                    chatFileInput.click(fn=craftor.add_to_prompt, inputs=[file_input, session_id], outputs=[chatbot, message])
        
        message.submit(fn=craftor.respond, inputs=[message, chatbot, session_id], outputs=[chatbot, message, output_df])
        clearButton.click(fn=craftor.clear_memory, inputs=session_id, outputs=chatbot)
        seeButton.click(fn= craftor.import_from_chat, inputs=session_id, outputs=output_df)
        return demo
