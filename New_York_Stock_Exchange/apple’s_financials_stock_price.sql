SELECT 
    f.*, 
    p.close AS stock_price
FROM 
    fundamentals f
JOIN 
    prices p 
    ON f.[Ticker Symbol] = p.symbol 
   AND f.[Period Ending] = p.date
WHERE 
    f.[Ticker Symbol] = 'AAPL';