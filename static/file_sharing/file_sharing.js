function getUploadTitle() {
    fake_path = document.getElementById('FileUpload1').value;
    document.getElementById('FileUploadLabel').innerHTML=fake_path.split("\\").pop();
  }