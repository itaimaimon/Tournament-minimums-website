// pages/api/calc.ts
import type { NextApiRequest, NextApiResponse } from "next";

type Data = {
  result?: string;
  message?: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  // Only allow POST
  if (req.method !== "POST") {
    return res.status(405).json({ message: "Method Not Allowed" });
  }

  try {
    // Forward the request body to the local Python FastAPI
    const pythonResponse = await fetch("http://127.0.0.1:8000/calculate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(req.body),
    });

    if (!pythonResponse.ok) {
      const text = await pythonResponse.text();
      throw new Error(`Python API error: ${text}`);
    }

    const data = await pythonResponse.json();

    // Return the Python API result
    return res.status(200).json({ result: data.result });
  } catch (error: any) {
    console.error("Error in /api/calc:", error.message);
    return res.status(500).json({ message: "Internal Server Error" });
  }
}

