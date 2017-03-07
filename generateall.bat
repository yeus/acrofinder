for %%f in (*.docx) do (

   echo %%~nf
   generate2 "%%~nf"
)