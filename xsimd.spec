# TODO: XTL xcomplex support? (BR: xtl-devel >= 0.7.0)
#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	C++ wrappers for SIMD intrinsics
Summary(pl.UTF-8):	Opakowanie C++ dla operacji SIMD
Name:		xsimd
Version:	10.0.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/xtensor-stack/xsimd/tags
Source0:	https://github.com/xtensor-stack/xsimd/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e0dfed5da51b0d34d02b42f5b2ddf830
URL:		https://xsimd.readthedocs.io/
BuildRequires:	cmake >= 3.1
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3-breathe
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SIMD (Single Instruction, Multiple Data) is a feature of
microprocessors that has been available for many years. SIMD
instructions perform a single operation on a batch of values at once,
and thus provide a way to significantly accelerate code execution.
However, these instructions differ between microprocessor vendors and
compilers.

xsimd provides a unified means for using these features for library
authors. Namely, it enables manipulation of batches of numbers with
the same arithmetic operators as for single values. It also provides
accelerated implementation of common mathematical functions operating
on batches.

%description -l pl.UTF-8
SIMD (Single Instruction, Multiple Data - jedna instrukcja, wiele
danych) to funkcjoalność mikroprocesorów dostępna od wielu lat.
Instrukcje SIMD wykonują pojedynczą operację na zbiorze wartości w
jednym czasie, zapewniając mozliwość znaczącego przyspieszenia
wykonywania kodu. Jednak instrukcje te różnią się w zależności od
producenta procesora i kompilatora.

xsimd udostępnia autorom bibliotek ujednolicone sposoby używania tych
funkcji. W szczególności xsimd pozwala operować na zbiorach liczb tymi
samymi operatorami, co na pojedynczych wartościach. Zapewnia także
akcelerowaną implementację popularnych funkcji matematycznych
operujących na zbiorach wartości.

%package devel
Summary:	C++ wrappers for SIMD intrinsics
Summary(pl.UTF-8):	Opakowanie C++ dla operacji SIMD
Group:		Development/Libraries
Requires:	libstdc++-devel

%description devel
SIMD (Single Instruction, Multiple Data) is a feature of
microprocessors that has been available for many years. SIMD
instructions perform a single operation on a batch of values at once,
and thus provide a way to significantly accelerate code execution.
However, these instructions differ between microprocessor vendors and
compilers.

xsimd provides a unified means for using these features for library
authors. Namely, it enables manipulation of batches of numbers with
the same arithmetic operators as for single values. It also provides
accelerated implementation of common mathematical functions operating
on batches.

%description devel -l pl.UTF-8
SIMD (Single Instruction, Multiple Data - jedna instrukcja, wiele
danych) to funkcjoalność mikroprocesorów dostępna od wielu lat.
Instrukcje SIMD wykonują pojedynczą operację na zbiorze wartości w
jednym czasie, zapewniając mozliwość znaczącego przyspieszenia
wykonywania kodu. Jednak instrukcje te różnią się w zależności od
producenta procesora i kompilatora.

xsimd udostępnia autorom bibliotek ujednolicone sposoby używania tych
funkcji. W szczególności xsimd pozwala operować na zbiorach liczb tymi
samymi operatorami, co na pojedynczych wartościach. Zapewnia także
akcelerowaną implementację popularnych funkcji matematycznych
operujących na zbiorach wartości.

%package apidocs
Summary:	API documentation for xsimd library
Summary(pl.UTF-8):	Dokumentacja API biblioteki xsimd
Group:		Documentation

%description apidocs
API documentation for xsimd library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki xsimd.

%prep
%setup -q

%build
install -d build
cd build
# fake LIBDIR so we can create noarch package
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_datadir}

%{__make}
cd ..

%if %{with apidocs}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc LICENSE README.md
%{_includedir}/xsimd
%{_npkgconfigdir}/xsimd.pc
%{_datadir}/cmake/xsimd

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_images,_static,api,*.html,*.js}
%endif
