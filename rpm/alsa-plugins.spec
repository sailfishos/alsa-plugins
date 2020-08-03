Name:       alsa-plugins
Summary:    The Advanced Linux Sound Architecture (ALSA) Plugins
Version:    1.2.2
Release:    1
License:    GPLv2+ and LGPLv2+
URL:        http://www.alsa-project.org/
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libpulse)

%description
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.
This package includes plugins for ALSA.


%package pulseaudio
Summary:    Alsa to PulseAudio backend
License:    LGPLv2+
Requires:   pulseaudio

%description pulseaudio
This plugin allows any program that uses the ALSA API to access a PulseAudio
sound daemon. In other words, native ALSA applications can play and record
sound across a network. There are two plugins in the suite, one for PCM and
one for mixer control.


%prep
%autosetup -n %{name}-%{version}/%{name}

%build

%reconfigure --disable-static \
    --without-speex \
    --disable-samplerate

%make_build

%install
%make_install

for i in ctl_arcam_av ctl_oss pcm_oss pcm_usb_stream pcm_vdownmix pcm_upmix; do
rm %{buildroot}%{_libdir}/alsa-lib/libasound_module_${i}.so
done
rm %{buildroot}%{_datadir}/alsa/alsa.conf.d/50-arcam-av-ctl.conf
rm %{buildroot}%{_datadir}/alsa/alsa.conf.d/50-oss.conf
rm %{buildroot}%{_datadir}/alsa/alsa.conf.d/60-upmix.conf
rm %{buildroot}%{_datadir}/alsa/alsa.conf.d/60-vdownmix.conf
rm %{buildroot}%{_datadir}/alsa/alsa.conf.d/98-usb-stream.conf
mv %{buildroot}%{_sysconfdir}/alsa/conf.d/99-pulseaudio-default.conf.example \
%{buildroot}%{_sysconfdir}/alsa/conf.d/99-pulseaudio-default.conf


%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files pulseaudio
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/README-pulse
%{_libdir}/alsa-lib/libasound_module_pcm_pulse.so
%{_libdir}/alsa-lib/libasound_module_ctl_pulse.so
%{_libdir}/alsa-lib/libasound_module_conf_pulse.so
%dir %{_sysconfdir}/alsa/conf.d
%{_sysconfdir}/alsa/conf.d/*.conf
%{_datadir}/alsa/alsa.conf.d/*.conf
