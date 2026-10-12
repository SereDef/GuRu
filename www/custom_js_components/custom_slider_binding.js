(function() {
    // Use py_shiny for Shiny for Python
    const binding = new Shiny.InputBinding();

    // binding.find = function(scope) {
    //     return scope.querySelectorAll('.discrete-slider');
    // };
    binding.find = function(scope) {
        return $(scope).find('.discrete-slider').toArray();
    };

    binding.getValue = function(el) {
        if (el.noUiSlider) {
            const labels = JSON.parse(el.getAttribute('data-labels'));
            const values = el.noUiSlider.get(true);
            const minIdx = Math.round(values[0]);
            const maxIdx = Math.round(values[1]);
            return labels.slice(minIdx, maxIdx + 1);
        }
        return [];
    };

    binding.subscribe = function(el, callback) {
        if (el.noUiSlider) {
            // noUiSlider calls the handler with (values, handle, ...); don't forward
            // those to Shiny's callback, which expects input options, not slider values.
            el.noUiSlider.on('update', function() { callback(); });
        }
    };

    window.Shiny.inputBindings.register(binding, 'nouislider.discreteSlider');

})();
