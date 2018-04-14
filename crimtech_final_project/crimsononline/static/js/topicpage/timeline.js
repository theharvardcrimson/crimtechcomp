window.addEventListener('load', function timelineOnLoad() {

  function DEBUG(str) {
    if (false) console.log(str);
  }

  var DateUtil = new (function newDateUtil() {
    this.monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
                      "Aug", "Sep", "Oct", "Nov", "Dec"];
    this.getMonthStr = function getMonthStr(d) {
      return this.monthNames[d.getMonth()];
    };
  })();

  function ScrollThrottler(callback) {
    var isRunning = true;
    var isDead = false;
    // Throttle scroll handling
    var lastScroll = Number.NEGATIVE_INFINITY;
    var handleScroll = function handleScroll() {
      if (window.scrollY != lastScroll) {
        // Scroll occurred
        if (callback && isRunning) callback();
        lastScroll = window.scrollY;
      }
      if (!isDead) requestAnimationFrame(handleScroll);
    }
    handleScroll();

    this.pause = function scrollThrottlerPause() {
      isRunning = false;
    };

    this.play = function scrollThrottlerPlay() {
      isRunning = true;
    };

    this.stop = function scrollThrottlerStop() {
      isDead = true;
    };
  };

  function cssPercent(num) {
    return String(Math.round(num * 100)) + '%';
  }

  var timelineElem = document.querySelector('.timeline-container');

  var timeline = (function Timeline(elem) {
    var self = this;
    var $elem = $(elem);
    var offsetTop = $elem.offset().top;
    var popup = elem.querySelector('.timeline__popup');
    var $popup = $(popup);

    var timelineEntries =
      [].slice.call(elem.querySelectorAll('*[data-timeline-entry]'))
      .map(function timelineEntriesMap(entryElem) {
        var secFromEpoch =
          Number(entryElem.getAttribute('data-timeline-entry-date'));
        return {
          id: entryElem.getAttribute('data-timeline-entry-id'),
          title: entryElem.getAttribute('data-timeline-entry-title'),
          date: new Date(secFromEpoch * 1000),
          elem: entryElem,
          $elem: $(entryElem)
        };
      })
      .map(function timelineEntryMapLinked(entry) {
        var linked = document.querySelector(
          '*[data-timeline-entry-linked=' + entry.id + ']');
        var $linked = $(linked);
        return $.extend({
          linked: linked,
          $linked: $linked,
          linkedTop: $linked.offset().top,
          linkedHeight: $linked.height()
        }, entry);
      })
      .sort(function timelineEntriesSort(e1, e2) {
        return 1;
      });

    var hasEntries = function hasEntries() {
      return timelineEntries.length > 1;
    };

    var focusEntry = function focusEntry(id) {
      timelineEntries.forEach(function (entry) {
        entry.$elem.removeClass('timeline__entry--focused');
      });
      var focusedEntry = id.hasOwnProperty('$elem')
        ? id
        : timelineEntries.find(function (entry) { return entry.id == id; });
      if (!focusedEntry) return;
      focusedEntry.$elem.addClass('timeline__entry--focused');
      popup.style.top =
        String(focusedEntry.$elem.position().top + focusedEntry.$elem.height() * 2) + "px";
      popup.style.left =
        String(focusedEntry.$elem.position().left - $popup.width() / 2) + "px";
      var focusedDate = focusedEntry.date;
      var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
                        "Aug", "Sep", "Oct", "Nov", "Dec"];
      popup.innerHTML =
        DateUtil.getMonthStr(focusedDate) + " "
        + focusedDate.getDate() + ", "
        + focusedDate.getFullYear();
    };

    var handleLinkedScroll = function handleLinkedScroll() {
      var windowMiddleY = window.scrollY + $(window).height() / 2;
      DEBUG(windowMiddleY);
      var activeTimelineEntry = timelineEntries[0];
      for (var i = timelineEntries.length - 1; i >= 0; --i) {
        var entry = timelineEntries[i];
        if (entry.linkedTop < windowMiddleY) {
          activeTimelineEntry = entry;
          break;
        }
      }
      if (window.scrollY > offsetTop) {
        $elem.addClass('timeline-container--floating');
      } else {
        $elem.removeClass('timeline-container--floating');
      }
      if (activeTimelineEntry) {
        DEBUG('Focused on: ' + activeTimelineEntry.title);
        timeline.focusEntry(activeTimelineEntry);
      }
    }

    if (hasEntries()) {
      var timelineWidth = $elem.width();
      var maxDate = timelineEntries[0].date,
          minDate = timelineEntries[timelineEntries.length - 1].date;
      var duration = maxDate - minDate;
      timelineEntries.forEach(function timelineEntriesSetup(entry) {
        var fractionOfTimeline =  ((entry.date - minDate) / duration);
        entry.$elem.css('left', cssPercent(fractionOfTimeline));
        entry.elem.addEventListener('click', function (event) {
          event.preventDefault();
          $('html, body').animate({
            scrollTop: entry.$linked.offset().top - $(window).height() / 3
          }, 500);
        });
      });
      $elem.removeClass('timeline-container--hide');
    }

    return {
      hasEntries: hasEntries,
      focusEntry: focusEntry,
      handleLinkedScroll: handleLinkedScroll
    };
  })(timelineElem);

  if (timeline.hasEntries()) {
    var scrollHandler = new ScrollThrottler(timeline.handleLinkedScroll);
  }
});
