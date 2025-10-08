document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.discrete-slider').forEach(function(slider) {
        const labels = JSON.parse(slider.getAttribute('data-labels'));
        const minVal = 0;
        const maxVal = labels.length - 1;

        if (!slider.noUiSlider) {
            noUiSlider.create(slider, {
                start: [labels[minVal], labels[maxVal]],
                connect: true,
                step: 1,
                range: {
                    min: minVal,
                    max: maxVal
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