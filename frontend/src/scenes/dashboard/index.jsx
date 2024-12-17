import { useState, useEffect } from "react";
import { Box, Button, Typography, useTheme, Select, MenuItem } from "@mui/material";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import LineChart from "../../components/LineChart";
import StatBox from "../../components/StatBox";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import ShowChartIcon from "@mui/icons-material/ShowChart";
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  // State to hold fetched data
  const [actualData, setActualData] = useState([]);
  const [predictedData, setPredictedData] = useState([]);
  const [dates, setDates] = useState([]);
  const [evalMetrics, setEvalMetrics] = useState({});
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");

  useEffect(() => {
    // Fetch the stock data from the API
    fetch('http://127.0.0.1:8000/') // Use HTTP instead of HTTPS
      .then(response => response.json())
      .then(data => {
        // Transform the dictionary into an array of objects
        const companyArray = Object.entries(data.stock_companies).map(([key, value]) => ({
          key,
          value
        }));
        setCompanies(companyArray);
        setSelectedCompany(companyArray[0]?.key || '');
        setActualData(data.actual_data);
        setPredictedData(data.predictions);
        setEvalMetrics(data.evaluation);
        setDates(data.dates);
      })
      .catch(error => console.error('Error:', error)); // Log errors
  }, []);



  // Handle dropdown selection change
  const handleChange = (event) => {
    const pc = selectedCompany;
    setSelectedCompany(event.target.value);
    fetch(`http://127.0.0.1:8000/stocks/${event.target.value}`)
      .then(response => response.json())
      .then(data => {
        setActualData(data.actual_data);
        setPredictedData(data.predictions);
        setEvalMetrics(data.evaluation);
        setDates(data.dates);
      })
      .catch(error => {
        console.error('Error:', error);
        setSelectedCompany(pc);
      });
  };

  const handleDownload = () => {
    const data = {
      selectedCompany,
      actualData,
      predictedData,
      dates,
      evalMetrics,
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${selectedCompany}_data.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };


  return (
    <Box m="20px">   

      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="" subtitle="Welcome to your dashboard" />

        {/* Dropdown for selecting company */}
        <Box>
          <Select
            value={selectedCompany}
            onChange={handleChange}
            displayEmpty
            sx={{
              backgroundColor: colors.primary[400],
              width: "400px",
              color: colors.grey[100],
              fontSize: "14px",
              fontWeight: "bold",
              padding: "5px 10px",
              borderRadius: "5px",
            }}
          >
            {companies.map((company) => (
              <MenuItem key={company.key} value={company.key}>
                {company.value}
              </MenuItem>
            ))}
          </Select>
        </Box>

        <Box>
          <Button
            sx={{
              backgroundColor: colors.blueAccent[700],
              color: colors.grey[100],
              fontSize: "14px",
              fontWeight: "bold",
              padding: "10px 20px",
            }}
            onClick={handleDownload}
          >
            <DownloadOutlinedIcon sx={{ mr: "10px" }} />
            Download Reports
          </Button>
        </Box>
      </Box>

      {/* Selected company display */}
      <Box mt="20px">
        <Typography variant="h5" color={colors.grey[100]}>
          Selected Company: {selectedCompany}
        </Typography>
      </Box>

      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="140px"
        gap="20px"
      >
          <Box
            gridColumn="span 3"
            backgroundColor={colors.primary[400]}
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            <StatBox
              title="MAE"
              subtitle="Mean Absolute Error"
              progress="0.75"
              increase={(evalMetrics["mae"] ?? 0.0).toFixed(3)}
              icon={
                <ErrorOutlineIcon
            sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
                />
              }
            />
          </Box>
          
          <Box
            gridColumn="span 3"
            backgroundColor={colors.primary[400]}
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            <StatBox
              title="MSE"
              subtitle="Mean Squared Error"
              progress="0.50"
              increase={(evalMetrics["mse"] ?? 0.0).toFixed(3)}
              icon={
                <ErrorOutlineIcon
            sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
                />
              }
            />
          </Box>
          <Box
            gridColumn="span 3"
            backgroundColor={colors.primary[400]}
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            <StatBox
              title="MAPE"
              subtitle="Mean Absolute Percentage Error"
              progress="0.30"
              increase={(evalMetrics["mape"] ?? 0.0).toFixed(3)}
              icon={
                <ErrorOutlineIcon
            sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
                />
              }
            />
          </Box>
          <Box
            gridColumn="span 3"
            backgroundColor={colors.primary[400]}
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            <StatBox
              title="R2"
              subtitle="R-Squared"
              progress="0.80"
              increase={(evalMetrics["r2"] ?? 0.0).toFixed(3)}
              icon={
                <ShowChartIcon
            sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
                />
              }
            />
          </Box>

          {/* ROW 2 */}
        <Box
          gridColumn="span 12"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
          height="70vh"
        >
          <Box display="flex" flexDirection="column" flex="1" mr="16px">
            <Box
              backgroundColor={colors.primary[400]}
              display="flex"
              alignItems="center"
              justifyContent="center"
              mb="16px"
            >
              <StatBox
                title="Variance"
                subtitle="Variance in Actual Data"
                progress="0.60"
                increase={(evalMetrics["variance"] ?? 0.0).toFixed(3)}
                icon={
                  <ShowChartIcon
                    sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
                  />
                }
              />
            </Box>
            <Box
              backgroundColor={colors.primary[400]}
              display="flex"
              alignItems="center"
              justifyContent="center"
            >
              <StatBox
                title="Accuracy"
                subtitle="Prediction Accuracy"
                progress="0.85"
                increase={(100 - (evalMetrics["mape"] ?? 0.0)*100).toFixed(3)}
                icon={
                  <ShowChartIcon
                    sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
                  />
                }
              />
            </Box>
          </Box>
          <Box flex="4" width="100%" height="100%">
            <Box
              mt="40px"
              p="20px 30px"
              display="flex"
              justifyContent="space-between"
              alignItems="center"
            >
              <Typography variant="h5" fontWeight="600" color={colors.grey[100]}>
                Actual vs Prediction Graph
              </Typography>
            </Box>
            <Box height="calc(100% - 100px)" m="-20px 0 0 0">
              <LineChart
                isDashboard={true}
                actualData={actualData}
                predictedData={predictedData}
                dates={dates}
              />
            </Box>
          </Box>
        </Box>

      </Box>
    </Box>
  );
};

export default Dashboard;
