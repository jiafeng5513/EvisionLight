#pragma once
#include <boost/signals2.hpp>
//-----------------------------------------------------------------------------
// Observable mixin.
//-----------------------------------------------------------------------------
// Convenience wrapper for boost::signals2::signal.
template<typename Signature> class Observer 
{
public:
  Observer(const Observer&) = delete;
  Observer& operator=(const Observer&) = delete;
  Observer() = default;
 
private:
  template<typename Observers> friend class Observable;
 
  using Signal = boost::signals2::signal<Signature>;
  using SignalResult = typename Signal::result_type;
 
  Signal signal_;
};
