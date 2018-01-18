$(function() {
            const sliders = document.querySelectorAll('input[type=range]');

            $(sliders).each(function () {
                var _this = $(this);
                _this.rangeslider({
                    polyfill: false,
                    onSlideEnd: function (position, value) {
                        $.post("{{ url_for('.set_brightness') }}",
                            {
                                ip_address: _this.attr('id'),
                                token: _this.data('token'),
                                port: _this.data('port'),
                                brightness: value
                            }
                        )
                    }
                });
            });
        });