SELECT 
    s.[GICS Sector], 
    AVG(f.[Total Revenue]) as avg_revenue
FROM 
    fundamentals f
JOIN 
    securities s ON f.[Ticker Symbol] = s.[Ticker symbol]
GROUP BY 
    s.[GICS Sector]