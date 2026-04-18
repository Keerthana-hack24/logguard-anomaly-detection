## **LogGuard: AI-Powered Login Anomaly Detection**:

<img width="600" height="200" alt="Screenshot 2026-04-18 170603" src="https://github.com/user-attachments/assets/81c227f8-75dc-45d9-9217-ed1e050d8808" />



This is a machine-learning system that is built to identify anomalies which in this case are suspicious login attempts from authentication logs.
This system mimics a basic classifier model that is used to classify risks in an SIEM. This project analyzes user login patterns, engineer behavioural features,
and applies the anomaly detection model to identify potentially malicious activity such as account takeovers or brute force login attempts.

**Important note**: The model was trained in an unsupervised environment, simulating a zero-day scenario where prior labels of 'attack' vs. 'normal' are unavailable

This project also includes a dashboard that displays the flagged users to help understand the investigation better for analysts.

## **Project Overview:**
In modern authentication systems, the large volume of data makes it difficult for manual detection. LogGuard addresses this problem by applying behavioural analytics and machine learning to identify patterns and flag abnormal users.

## **Tech Stack**: Python | Pandas | Scikit-Learn (Isolation Forest) | Streamlit | Matplotlib

## **Key Features:**
• Behavioral feature engineering from login activity logs
• Entropy-based diversity metrics for IP addresses, countries, and devices
• Isolation Forest anomaly detection model
• Risk scoring system to prioritize suspicious users
• Interactive Streamlit dashboard for security analysis
• Visualization of anomalous behavior patterns

## **System Architecture:**

<img width="383" height="513" alt="image" src="https://github.com/user-attachments/assets/fd39b54b-c808-4c76-8ce6-700b9ecea550" />





## **Parsing the dataset:**

The main challenge while doing this project was that the original dataset has around 33 million records, so only around 1 million rows were used which was created in the form of parsed_logs.csv. Further, a sampling technique was applied on this csv file to take records of 1000 users and store all their records in the form of parsed_logs_sample.csv (this can be found in the data/). Sampling 1000 random users in this way without taking random records ensured the key principle of cybersecurity analysis:

"An individual log is baseless, but the real analysis comes from the pattern of logs"

## **Machine Learning Model:**

The project uses Isolation Forest, an unsupervised anomaly detection algorithm.
Isolation Forest works by randomly partitioning the feature space and identifying observations that can be isolated quickly. Anomalous behavior typically requires fewer splits to isolate, resulting in higher anomaly scores.

• Algorithm: Isolation Forest
• Contamination rate: 5%
• Trees: 100

The model produces:
• Anomaly labels (normal vs suspicious)
• Anomaly scores
• Risk scores scaled from 0–100


## **Feature Engineering**:

User behavior is summarized using aggregated features such as:
• Login Activity
• Login attempt count
• Failed login ratio
• Login rate per hour
• Activity span
• Network Diversity
• Unique IP addresses used
• Unique countries accessed
• IP entropy
• Country entropy
• Device Behavior
• Unique device types
• Device entropy

These features capture patterns that may indicate abnormal or suspicious login behavior.


## **Dataset**:
This project was developed using authentication log data derived from the RBA dataset. Because the original dataset is very large, this repository includes a reduced sample for demonstration and reproducibility:
https://www.kaggle.com/datasets/dasgroup/rba-dataset


## **Future Improvements:**

1. Evaluating model predictions against labeled attack data
2. Incorporating temporal sequence modeling
3. Deploying the dashboard for public access
4. Integrating the system with real-time log pipelines
5. Experimenting with additional anomaly detection models

**Acknowledgment:**
The core data pipeline, feature engineering, and anomaly detection system were implemented independently. AI tools were used to assist with refining the Streamlit dashboard interface and presentation.

