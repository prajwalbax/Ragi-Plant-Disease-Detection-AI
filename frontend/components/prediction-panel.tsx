"use client";

import Image from "next/image";
import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { RotateCcw, ScanLine, UploadCloud, X } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { toast } from "sonner";

import {
  predictDisease,
  type PredictionResponse,
} from "@/lib/api";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

const maxFileSize = 8 * 1024 * 1024;

export function PredictionPanel() {

  const [file,setFile] =
  useState<File|null>(null);

  const [result,setResult] =
  useState<PredictionResponse|null>(
    null
  );

  const [error,setError] =
  useState("");

  const [loading,setLoading] =
  useState(false);

  const previewUrl =
  useMemo(

    ()=>(

      file

      ?

      URL.createObjectURL(
        file
      )

      :

      ""

    ),

    [file]

  );

  const onDrop = (

    acceptedFiles: File[]

  ) => {

    const nextFile =
    acceptedFiles[0];

    if(!nextFile){

      return;

    }

    setFile(nextFile);

    setResult(null);

    setError("");

    toast.success(
      "Image ready"
    );

  };

  const {

    getRootProps,

    getInputProps,

    isDragActive

  } = useDropzone({

    onDrop,

    accept:{

      "image/*":[

        ".jpg",

        ".jpeg",

        ".png",

        ".webp"

      ]

    },

    maxFiles:1,

    maxSize:maxFileSize,

    onDropRejected:()=>{

      toast.error(

        "Upload JPG/PNG/WEBP under 8MB"

      );

    }

  });

  async function analyze(){

    if(!file){

      toast.error(

        "Upload image first"

      );

      return;

    }

    setLoading(true);

    setResult(null);

    setError("");

    try{

      const prediction =

      await predictDisease(
        file
      );

      setResult(
        prediction
      );

      toast.success(
        "Prediction complete"
      );

    }

    catch(err){

      const message =

      err instanceof Error

      ?

      err.message

      :

      "Prediction failed";

      setError(
        message
      );

      toast.error(
        message
      );

    }

    finally{

      setLoading(false);

    }

  }

  function reset(){

    setFile(null);

    setResult(null);

    setError("");

  }

  return(

<motion.section

initial={{

opacity:0,

scale:0.98

}}

animate={{

opacity:1,

scale:1

}}

className="
rounded-lg
border
border-white/10
bg-card
p-5
shadow-glow
backdrop-blur-2xl
"

>

<div className="
mb-5
flex
justify-between
">

<div>

<h2 className="
text-xl
font-semibold
">

Prediction Interface

</h2>

<p className="
text-sm
text-muted
">

Upload a ragi leaf image

</p>

</div>

<Button

variant="ghost"

size="icon"

onClick={reset}

>

<RotateCcw/>

</Button>

</div>

<div

{...getRootProps()}

className={cn(

"grid min-h-64 place-items-center rounded-lg border border-dashed p-5",

isDragActive

?

"border-primary bg-primary/10"

:

"border-white/15"

)}

>

<input

{...getInputProps()}

/>

{

previewUrl

?

<div className="
relative
h-72
w-full
overflow-hidden
rounded-lg
">

<Image

src={previewUrl}

alt="leaf"

fill

className="
object-cover
"

/>

<button

onClick={(e)=>{

e.stopPropagation();

reset();

}}

className="
absolute
right-3
top-3
"

>

<X/>

</button>

</div>

:

<div>

<UploadCloud

className="
mx-auto
mb-3
h-10
w-10
"

/>

<p>

Drag image

</p>

</div>

}

</div>

<Button

className="
mt-5
w-full
"

onClick={analyze}

disabled={

loading

||

!file

}

>

<ScanLine/>

{

loading

?

"Analyzing..."

:

"Analyze"

}

</Button>

{

loading &&

<div className="
mt-5
space-y-3
">

<Skeleton

className="
h-6
w-1/2
"

/>

<Skeleton

className="
h-20
w-full
"

/>

</div>

}

{

error &&

<div className="
mt-5
rounded-lg
bg-red-500/10
p-4
">

{error}

</div>

}

{

result && (

<motion.div

initial={{

opacity:0,

y:10

}}

animate={{

opacity:1,

y:0

}}

className="
mt-5
space-y-5
rounded-lg
border
border-primary/20
bg-primary/10
p-5
"

>

<div>

<p className="
text-primary
text-sm
uppercase
">

Prediction

</p>

<h3 className="
text-3xl
font-bold
capitalize
">

{

result.class

}

</h3>

<p>

Confidence

{" "}

{

result
.confidence_percent
.toFixed(2)

}%

</p>

</div>

<div>

<p className="
text-muted
">

{

result.description

}

</p>

</div>

{

result.advisory && (

<>

<div className="
rounded-lg
border
border-white/10
bg-black/20
p-4
">

<h4 className="
mb-3
font-semibold
text-primary
">

English

</h4>

{

result
.advisory
.english_explanation
?.map(

(line,index)=>(

<p
key={index}
>

• {line}

</p>

)

)

}

</div>

<div className="
rounded-lg
border
border-white/10
bg-black/20
p-4
">

<h4 className="
mb-3
font-semibold
text-primary
">

ಕನ್ನಡ

</h4>

{

result
.advisory
.kannada_explanation
?.map(

(line,index)=>(

<p
key={index}
>

• {line}

</p>

)

)

}

</div>

<div className="
rounded-lg
border
border-green-500/20
bg-green-500/10
p-4
">

<h4 className="
mb-3
font-semibold
text-green-300
">

Recommendation

</h4>

<p>

Chemical:

{" "}

{

result
.advisory
.recommendation
?.chemical_name

||

"N/A"

}

</p>

<p>

Dosage:

{" "}

{

result
.advisory
.recommendation
?.dosage

||

"N/A"

}

</p>

<p>

Application:

{" "}

{

result
.advisory
.recommendation
?.application_method

||

"N/A"

}

</p>

</div>

</>

)

}

</motion.div>

)

}

</motion.section>

);

}