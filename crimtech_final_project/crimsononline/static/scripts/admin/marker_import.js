// Batch importing of map markers from a local CSV

(function ($) {
  // TODO: Upgrade to the latest Maps API and find a better way to
  // throttle requests.
  var GEOCODE_DELAY = 2000;

  var $markerImportFileField;

  function getMarkersField(name, index) {
    return $("#id_markers-" + index + "-" + name);
  }

  function addMarkersRow() {
    $("#markers-group").find(".add-row").find("a").click();
    return $("#markers-group").find(".empty-form").prev();
  }

  function loadMarkerFile() {
    var file;
    if ((file = this.files[0])) {
      Papa.parse(file, {
        header: true,
        complete: function (csv) {
          csv.data.forEach(function (marker, i) {
            setTimeout(function () { addMarker(marker) }, i * GEOCODE_DELAY);
          });
        }
      });
    }
  }

  function addMarker(marker) {
    var row = addMarkersRow(),
      rowIndex = row.attr("id").match(/\-(\d+)$/)[1];

    Object.keys(marker).forEach(function (key) {
      getMarkersField(key, rowIndex).val(marker[key]);
    });

    if (marker.address) {
      geocoder.getLatLng(marker.address, function (location) {
        if (!location) {
          location = {
            lat: function () { return "failed"; },
            lng: function () { return "failed"; }
          }
        }

        getMarkersField("lat", rowIndex).val(location.lat());
        getMarkersField("lng", rowIndex).val(location.lng());
      });
    }
  }

  if (!window.File || !window.FileReader) {
    $markerImportFileField.replaceWith("Please upgrade to a modern " +
      "browser to use this feature.");
    return;
  }

  $(function () {
    $markerImportFileField = $("#id_marker_import_file");
    $markerImportFileField.change(loadMarkerFile);
  });
})(django.jQuery);
