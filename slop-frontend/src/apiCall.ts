/**
 * Call the detection API to analyze a page URL
 * @returns A promise that resolves to a float score
 */
import axios from "axios";


// try {
//         const response = await axios.post(`${API_URL}/exercises`, exerciseData, {
//             headers: {
//                 Authorization: `Bearer ${token}`,
//             },
//         });
//         return response.data;
//     }
//     catch (error) {
//         console.log("Create exercise error: ", error);
//         throw error;
//     }

export async function detectPage(url: string): Promise<number> {
    try {
        const response = await axios.post(
            "http://localhost:8000/detect/page",
            { url },
            { headers: { "Content-Type": "application/json" } }
        );
        return response.data.percentage;
    } catch (error) {
        console.error("Error detecting page:", error);
        throw error;
    }
}

// export async function detectPage(url: string): Promise<number> {
//   try {
//     const response = await fetch("http://localhost:8000/detect/page", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ url }),
//     });

//     if (!response.ok) {
//       throw new Error(`API error: ${response.status} ${response.statusText}`);
//     }

//     const data = await response.json();

//     // Assuming the API returns a JSON object with a score field
//     if (typeof data === "number") {
//       return data;
//     } else if (typeof data.score === "number") {
//       return data.score;
//     } else {
//       throw new Error("Invalid response format: expected a number or object with score field");
//     }
//   } catch (error) {
//     console.error("Error calling detection API:", error);
//     throw error;
//   }
// }
