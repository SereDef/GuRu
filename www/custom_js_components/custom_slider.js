document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.discrete-slider').forEach(function(slider) {
        const labels = JSON.parse(slider.getAttribute('data-labels'));

        if (!slider.noUiSlider) {
            noUiSlider.create(slider, {
                start: [labels[0], labels[labels.length - 1]],
                connect: true,
                step: 1,
                range: {
                    min: 0,
                    max: labels.length - 1
                },
                tooltips: [true, true],
                format: {
                    to: function(value) { return labels[Math.round(value)]; },
                    from: function(value) { return labels.indexOf(value); }
                },
                pips: {
                    mode: 'steps',
                    density: 100,
                    format: {
                        to: function(value) { return labels[value]; }
                    }
                }
            });
        }
    });
});