const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const maxUploadfile = 7;
const maxfilesize = 1024 * 1024 * 1024;
let fileCount = 0;
let addedFiles = 0;

function getCheckCode() {
  return $("#check_code").val();
}

function getDocumentId() {
  return $("#document_id").val();
}

function site_add_cancel() {
  if (confirm("문서등록을 취소하시겠습니까?") == true) {
    location.href = "/sites/";
  } else {
    return false;
  }
}

$(document).ready(init());

let transfer;

function init() {
  $.ajax({
    type: "GET",
    url: "/common/member/info/",
    dataType: "json",
    success: function (data) {
      const memberInfo = data["members_data"];
      let settings = {
        tabNameText: "권한자 선택",
        rightTabNameText: "선택된 권한자",
        searchPlaceholderText: "검 색",
        groupDataArray: memberInfo,
        groupItemName: "groupName",
        groupArrayName: "groupData",
        itemName: "name",
        valueName: "value",
        callable: function (items) {
          console.log(items);
        },
      };
      transfer = $(".member_permission").transfer(settings);
    },
  });
}

function site_reg_document() {
  const acceptPermissionMember = transfer.getSelectedItems();
  const serializeData = JSON.stringify(acceptPermissionMember);

  if ($("#project").val() == "") {
    alert("프로젝트를 선택하세요");
    return false;
  }

  if (acceptPermissionMember.length == 0) {
    alert("문서등록에 대한 권한자를 선택해주세요");
    return null;
  }

  param = {};
  param.project = $("#project").val();
  param.kind = $("#kind").val();
  param.permission = serializeData;

  $.ajax({
    type: "POST",
    url: "/sites/document/reg/",
    headers: { "X-CSRFToken": csrfToken },
    dataType: "json",
    data: param,
    success: function (data) {
      if (data.success) {
        $("#document_id").val(data.document_id);
        $("#fine-uploader-manual-trigger").fineUploader("uploadStoredFiles");
      } else {
        alert("문서등록 작업이 정상적으로 이루어 지지 않았습니다-0.");
      }
    },
    error: function (request, status, error) {
      alert("문서등록 작업이 정상적으로 이루어 지지 않았습니다-1.");
    },
  });
}

$("#submit-btn").click(function (event) {
  event.preventDefault();
  if (fileCount == 0) {
    if (!confirm("첨부 파일이 없습니다. 그대로 진행 하시겠습니까?")) return;
  }
  if (confirm("파일을 업로드하시겠습니까?")) site_reg_document();
});

$("#fine-uploader-manual-trigger").fineUploader({
  template: "qq-template-manual-trigger",
  debug: false,
  autoUpload: false,
  maxConnections: maxUploadfile,
  validation: {
    allowedExtensions: [
      "pptx",
      "ppt",
      "doc",
      "docx",
      "xls",
      "xlsx",
      "jpg",
      "jpeg",
      "png",
      "gif",
      "pdf",
      "zip",
      "txt",
      "log",
    ],
    allowEmpty: false,
    itemLimit: maxUploadfile,
    sizeLimit: maxfilesize,
  },
  messages: {
    typeError: "업로드가 불가능 한 확장자 파일 입니다, {file}.",
    sizeError: "파일 사이즈는 10M를 넘을 수 없습니다, {file}",
  },
  request: {
    endpoint: "/sites/document/upload/apply/",
    customHeaders: {
      "X-SCRF-TOKEN": csrfToken,
    },
    params: {
      document_id: getDocumentId,
      check_code: getCheckCode,
    },
  },

  callbacks: {
    onComplete: function (id, fileName, responseJSON) {
      if (responseJSON.success) {
        addedFiles++;
        if (addedFiles == fileCount) {
          alert("문서등록이 완료되었습니다.");
          location.href = "/sites/";
        }
      } else {
        alert(
          "파일 업로드에 실패하였습니다. 다시 시도하여주세요." +
            responseJSON.error
        );
      }
    },
    onError: function () {
      // alert("파일 업로드에 실패하였습니다. 다시 시도하여주세요");
      // location.href = "/sites/document/upload/";
      // 파일 업로드 실패시 전체 삭제 루틴을 반영한다.
    },
    onSubmit: function (id, fileName, responseJSON) {
      fileCount++;
    },
    onCancel: function (id, filename) {
      fileCount--;
    },
  },
});
