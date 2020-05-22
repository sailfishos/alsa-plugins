Name:       alsa-plugins

Summary:    The Advanced Linux Sound Architecture (ALSA) Plugins
Version:    1.0.26
Release:    1
Group:      System/Libraries
License:    GPLv2+ and LGPLv2+
URL:        http://www.alsa-project.org/
Source0:    ftp://ftp.alsa-project.org/pub/plugins/%{name}-%{version}.tar.bz2
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libpulse)

%description
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.
This package includes plugins for ALSA.


%package pulseaudio
Summary:    Alsa to PulseAudio backend
License:    LGPLv2+
Group:      System/Libraries
Requires:   pulseaudio

%description pulseaudio
This plugin allows any program that uses the ALSA API to access a PulseAudio
sound daemon. In other words, native ALSA applications can play and record
sound across a network. There are two plugins in the suite, one for PCM and
one for mixer control.



%prep
%setup -q -n %{name}-%{version}

%build

%configure --disable-static \
    --without-speex \
    --disable-samplerate

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

find  %{buildroot}

for i in ctl_arcam_av ctl_oss pcm_oss pcm_usb_stream pcm_vdownmix pcm_upmix; do
rm ${RPM_BUILD_ROOT}%{_libdir}/alsa-lib/libasound_module_${i}.so
done
find  %{buildroot}
mv ${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d/99-pulseaudio-default.conf.example \
${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d/99-pulseaudio-default.conf

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
%{_datadir}/alsa/alsa.conf.d/*.conf
