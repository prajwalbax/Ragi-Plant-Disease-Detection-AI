import axios from "axios";


export type HealthResponse = {

  status: string;

  model_loaded?: boolean;

};


export type Recommendation = {

  chemical_name: string;

  dosage: string;

  application_method: string;

};


export type AdvisoryResponse = {

  english_explanation: string[];

  kannada_explanation: string[];

  recommendation: Recommendation;

};


export type PredictionResponse = {

  class: string;

  confidence: number;

  confidence_percent: number;

  description: string;

  filename: string;

  advisory: AdvisoryResponse;

};


const apiBaseUrl =

process.env
.NEXT_PUBLIC_API_URL;


export const api = axios.create({

  baseURL:

  apiBaseUrl || undefined,

  timeout: 45000,

});


export async function checkHealth():

Promise<HealthResponse> {

  if (!apiBaseUrl) {

    return {

      status:"offline",

      model_loaded:false

    };

  }

  try {

    const response =

    await api.get<HealthResponse>(

      "/health",

      {

        timeout:5000

      }

    );

    return response.data;

  }

  catch {

    return {

      status:"offline",

      model_loaded:false

    };

  }

}


export async function predictDisease(

  file: File

): Promise<PredictionResponse> {

  if (!apiBaseUrl) {

    throw new Error(

      "NEXT_PUBLIC_API_URL missing."
    );

  }

  const formData =

  new FormData();

  formData.append(

    "file",

    file

  );

  try {

    const response =

    await api.post<PredictionResponse>(

      "/predict",

      formData,

      {

        headers: {

          "Content-Type":

          "multipart/form-data"

        }

      }

    );

    return response.data;

  }

  catch (error) {

    if (

      axios.isAxiosError(

        error

      )

    ) {

      const detail =

      error.response
      ?.data
      ?.detail;

      throw new Error(

        typeof detail ===

        "string"

        ?

        detail

        :

        "Prediction failed."

      );

    }

    throw error;

  }

}