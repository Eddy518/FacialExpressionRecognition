// // const video = document.querySelector("#video");
// // const startCameraBtn = document.querySelector("#start-camera");
// const stopCameraBtn = document.querySelector("#stop-camera");
//
// // stopCameraBtn.addEventListener("click", () => alert("Hey"));
//
// document.addEventListener("DOMContentLoaded", () => {
//   let but = document.getElementById("start-camera");
//   let video = document.getElementById("video");
//   let mediaDevices = navigator.mediaDevices;
//   but.addEventListener("click", () => {
//     // Accessing the user camera and video.
//     mediaDevices
//       .getUserMedia({
//         video: true,
//         audio: true,
//       })
//       .then((stream) => {
//         // Changing the source of video to current stream.
//         video.srcObject = stream;
//         video.addEventListener("loadedmetadata", () => {
//           video.play();
//
//       })
//       .catch(alert);
//   });
//   stopCameraBtn.onclick = function () {
//     localStream.getVideoTracks()[0].stop();
//     video.src = "";
//
//     localStream.getAudioTracks()[0].stop();
//     audio.src = "";
//   };
// });
const videoContainer = document.querySelector(".video");

let cameraOnBool = false;
(function () {
  const video = document.querySelector("#video");

  const captureVideoButton = document.querySelector("#start-camera");
  const stopVideoButton = document.querySelector("#stop-camera");

  //Capture Video
  captureVideoButton.onclick = function () {
    document.getElementById('fileUpload').disabled = true;
    navigator.mediaDevices
      .getUserMedia({
        audio: true,
        video: true,
      })
      .then((stream) => {
        window.localStream = stream;
        video.srcObject = stream;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  stopVideoButton.onclick = function () {
    cameraOnBool = false;
    localStream.getVideoTracks()[0].stop();
    video.src = "";
    location.reload();
  };
})();

