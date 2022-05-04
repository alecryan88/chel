docker build -t nhl_dag:1.7 .

docker run -p 3000:3000 -e AWS_ACCESS_KEY_ID=your_key -e AWS_SECRET_ACCESS_KEY=your_key nhl_dag:tag